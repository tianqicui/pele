import numpy as np
import networkx as nx

from pygmin.landscape import Graph, LocalConnect
from pygmin.landscape._distance_graph import _DistanceGraph

__all__ = ["DoubleEndedConnect"]

                     


class DoubleEndedConnect(object):
    """
    Find a connected network of minima and transition states between min1 and min2
    
    Parameters
    ----------
    min1, min2 : Mimumum() objects
        the two minima to try to connect
    pot : potential object
        the potential
    mindist : callable
        the function which returns the optimized minimum distance between
        two structures
    database : Database() object
        the database object, used to save distance calculations so
        mindist() need only be called once for each minima pair. *Note* the
        use of this and graph is a bit redundant, this should be cleaned up
    use_all_min : bool
        if True, then all known minima and transition states in graph will
        be used to try to connect min1 and min2.  This requires a mindist()
        call (or a retrieveal operation from database) for every pair which
        can take a very long time if many minima are known.  
    verbosity : int
        this controls how many status messages are printed.  (not really
        implemented yet)
    merge_minima : bool
        if True, minima for which NEB finds no transition state candidates 
        between them will be merged
    max_dist_merge : float
        merging minima will be aborted if the distance between them is greater
        than max_dist_merge
    local_connect_params : dict
        parameters passed to the local connect algorithm.  This includes all
        NEB and all transition state search parameters, along with, e.g. 
        now many times to retry a local connect run.  See documentation for
        LocalConnect for details.
    fresh_connect : bool
        if true, ignore all existing minima and transition states in the
        database and try to find a new path
    longest_first : bool
        if true, always try to connect the longest segment in the path guess
        first
    
    Notes
    -----
    The algorithm is iterative, with each iteration composed of
    
    While min1 and min2 are not connected:
        1) choose a pair of known minima to try to connect
        
        2) use NEB to get a guess for the transition states between them
        
        3) refine the transition states to desired accuracy
        
        4) fall off either side of the transition states to find the two
        minima associated with that candidate
        
        5) add the transition state and associated minima to the known
        network
        
    
    Of the above, steps 1 and 2 and 3 are the most involved.  See the NEB and
    FindTransitionState classes for detailed descriptions of steps 2 and 3.
    
    An important note is that the NEB is used only to get a *guess* for the
    transition state.  Thus we only want to put enough time and energy into
    the NEB routine to get the guess close enough that FindTransitionState
    can refine it to the correct transition state.  FindTransitionState is
    very fast if the initial guess is good, but can be very slow otherwise.
    
    Choose a pair
    -------------
    Here I will describe step 1), the algorithm to find a pair of known
    minima to try to connect.  This choice will keep in mind that the
    ultimate goal is to connect min1 and min2.
    
    In addition to the input parameter "graph", we keep a second graph
    "Gdist" (now called "dist_graph") which also has minima as the vertices. Gdist has an edge
    between (almost) every minima. The edge weight between vertices u and v
    is
    
        if u and v are connected in "graph":
            weight(u,v) = 0.
        else:
            weight(u,v) = mindist(u,v)
    
    Also, edges are removed from Gdist when an NEB is done to try to
    connect them.  This is to ensure we don't repeat NEB runs over and over
    again.  The minimum weight path between min1 and min2 in Gdist gives a
    good guess for the best way to try connect min1 and min2.  So the
    algorithm to find a pair of know minima (trial1, trial2) to try to
    connect is 
    
    path = Gdist.minimum_weight_path(min1, min2)
    trial1, trial2 = minima pair in path with lowest nonzero edge weight

    todo:
        allow user to pass graph
        
    """    
    def __init__(self, min1, min2, pot, mindist, database, 
                 use_all_min=False, verbosity=1,
                 merge_minima=False, 
                 max_dist_merge=0.1, local_connect_params=dict(),
                 fresh_connect=False, longest_first=False,
                 ):
        self.minstart = min1
        assert min1._id == min1, "minima must compare equal with their id %d %s %s" % (min1._id, str(min1), str(min1.__hash__()))
        self.minend = min2
        self.pot = pot
        self.mindist = mindist
        self.pairsNEB = dict()
        self.longest_first = longest_first
        
        self.verbosity = int(verbosity)
        self.local_connect_params = dict([("verbosity",verbosity)] + local_connect_params.items())
        self.database = database
        self.fresh_connect = fresh_connect
        if self.fresh_connect:
            self.graph = Graph(self.database, minima=[self.minstart, self.minend])
        else:
            self.graph = Graph(self.database)

        self.merge_minima = merge_minima
        self.max_dist_merge = float(max_dist_merge)

        #check if a connection exists before initializing distance Graph
        if self.graph.areConnected(self.minstart, self.minend):
            print "minima are already connected.  not initializing distance graph"
            return

        self.dist_graph = _DistanceGraph(self.database, self.graph, self.mindist, self.verbosity)
        self.dist_graph.initialize(self.minstart, self.minend, use_all_min)
        
        print "************************************************************"
        print "starting a double ended connect run between"
        print "        minimum 1: id %d energy %f" % (self.minstart._id, self.minstart.energy)
        print "        minimum 2: id %d energy %f" % (self.minend._id, self.minend.energy)
        print "        dist %f" % self.getDist(self.minstart, self.minend)
        print "************************************************************"
        
    

    
    def mergeMinima(self, min1, min2):
        """merge two minimum objects
        
        This will delete min2 and make everything that
        pointed to min2 point to min1.
        """
        if False:
            print "MERGE MINIMA IS NOT WORKING YET"
            return
        #prefer to delete the minima with the large id.  this potentially will be easier
        if min2._id < min1._id:
            min1, min2 = min2, min1
        
        debug = False
        dist = self.getDist(min1, min2)
        print "merging minima", min1._id, min2._id, dist, "E1-E2", min1.energy - min2.energy

        #deal with the case where min1 and/or min2 are the same as minstart and/or minend
        #make sure the one that is deleted (min2) is not minstart or minend
        if ((min1 == self.minstart and min2 == self.minend) or 
            (min2 == self.minstart and min1 == self.minend)):
            print "ERROR: trying to merge the start and end minima.  aborting"
            return
        if min2 == self.minstart or min2 == self.minend:
            min1, min2 = min2, min1
        
        #print "min1 min2", min1, min2

        if dist > self.max_dist_merge:
            print "    minima merge aborted.  distance is too large", dist
            return
        
#        if debug:
#            #testing
#            if min2 in self.database.minima():
#                print "error, min2 is still in database"
#            for ts in self.database.transition_states():
#                if min2 == ts.minimum1 or min2 == ts.minimum2:
#                    print "error, a transition state attached to min2 is still in database", ts.minimum1._id, ts.minimum2._id
        
        #merge minima in transition state graph
        #note, this will merge minima in the database also
        self.graph.mergeMinima(min1, min2, update_database=True)
        if debug:
            #testing
            if min2 in self.graph.graph.nodes():
                print "error, min2 is still in self.graph.graph"
            print "self.graph.graph. nnodes", self.graph.graph.number_of_nodes()

        #merge minima in distance graph        
        self.dist_graph.mergeMinima(min1, min2)

    def getDist(self, min1, min2):
        """
        get the distance between min1 and min2.
        
        Try first to get distances from the dictionary distmatrix as this is 
        the fastest access method.  Then try to 
        get distances from the database if they exist, else calculate the
        distance and save it to the database and distmatrix
        """
        return self.dist_graph.getDist(min1, min2)

    def _addTransitionState(self, E, coords, min_ret1, min_ret2, eigenvec, eigenval):
        """
        add a transition state to the database, the transition state graph and
        the distance graph
        """
        #sanity check for the energies
        me1, me2 = min_ret1[1], min_ret2[1]
        if E < me1 or E < me2:
            print "warning: trying to add a transition state that has energy lower than it's minima."
            print "    TS energy", E, "minima energy", me1, me2
            print "    aborting"
            return False
        
        #add the minima to the transition state graph.  
        #This step is important to do first because it returns a Database Minimum object.
        min1 = self.graph.addMinimum(min_ret1[1], min_ret1[0])
        min2 = self.graph.addMinimum(min_ret2[1], min_ret2[0])
        if min1 == min2:
            print "warning: stepping off the transition state resulted in twice the same minima", min1._id
            return False
        
        

        print "adding transition state", min1._id, min2._id
        #update the transition state graph
        #this also updates the database and returns a TransitionState object
        ts = self.graph.addTransitionState(E, coords, min1, min2, eigenvec=eigenvec, eigenval=eigenval)
#        self.graph.refresh()

        #update the distance graph
        self.dist_graph.addMinimum(min1)
        self.dist_graph.addMinimum(min2)
        self.dist_graph.setTransitionStateConnection(min1, min2)

        if True:
            #print some information
            dse  = self.getDist(self.minend, self.minstart)
            msid = self.minstart._id
            meid = self.minend._id
            m1id = min1._id
            m2id = min2._id
            if min1 != self.minstart and min1 != self.minend:
                ds = self.getDist(min1, self.minstart)
                de = self.getDist(min1, self.minend)
                if ds < dse > de:
                    triangle = ""
                else: 
                    triangle = ": new minima not in between start and end"
                print "    distances: %4d -> %4d = %f    %4d -> %4d = %f    %4d -> %4d = %f  %s" % (msid, m1id, ds, m1id, meid, de, m1id, m2id, dse, triangle)
                #print "    dist new min 1 to minstart, minend ", ds, de, dse
            if min2 != self.minstart and min2 != self.minend:
                ds = self.getDist(min2, self.minstart)
                de = self.getDist(min2, self.minend)
                if ds < dse > de:
                    triangle = ""
                else: 
                    triangle = ": new minima not in between start and end"
                print "    distances: %4d -> %4d = %f    %4d -> %4d = %f    %4d -> %4d = %f" % (msid, m2id, ds, m2id, meid, de, m2id, m2id, dse)

        
        return True

    def _getLocalConnectObject(self):
        return LocalConnect(self.pot, self.mindist, **self.local_connect_params)

    def _localConnect(self, min1, min2):
        """
        1) NEB to find transition state candidates.  
        
        for each transition state candidate:
        
            2) refine the transition state candidates
        
            3) if successful, fall off either side of the transition state
            to find the minima the transition state connects. Add the new 
            transition state and minima to the graph 
        """
        #Make sure we haven't already tried this pair and
        #record some data so we don't try it again in the future
        if self.pairsNEB.has_key((min1, min2)):
            print "WARNING: redoing NEB for minima", min1._id, min2._id
            print "         aborting NEB"
            #self._remove_edgeGdist(min1, min2)
            self.dist_graph.removeEdge(min1, min2)
            return True
        self.pairsNEB[(min1, min2)] = True
        self.pairsNEB[(min2, min1)] = True
        
        #Make sure they're not already connected.  sanity test
        if self.graph.areConnected(min1, min2):
            print "in _local_connect, but minima are already connected. aborting", min1._id, min2._id, self.getDist(min1, min2)
            self.dist_graph.setTransitionStateConnection(min1, min2)
            self.dist_graph.checkGraph()
            return True
        
        #do local connect run
        local_connect = self._getLocalConnectObject()        
        res = local_connect.connect(min1, min2)

        #now add each new transition state to the graph and database.
        nsuccess = 0
        for tsret, m1ret, m2ret in res.new_transition_states:
            goodts = self._addTransitionState(tsret.energy, tsret.coords, m1ret, m2ret, tsret.eigenvec, tsret.eigenval)
            if goodts:
                nsuccess += 1
 
        #check results
        #nclimbing = len(climbing_images)
        #print "from NEB search found", nclimbing, "transition state candidates"
        if nsuccess == 0:
            dist = self.getDist(min1, min2)
            if dist < self.max_dist_merge:
                print "WARNING: local connect failed and the minima are close. Are the minima really the same?"
                print "         energies:", min1.energy, min2.energy, "distance", dist 
                if self.merge_minima:
                    self.mergeMinima(min1, min2)
                else:
                    print "         set merge_minima=True to merge the minima" 
                return False   


        #remove this edge from Gdist so we don't try this pair again again
        #self._remove_edgeGdist(min1, min2)
        self.dist_graph.removeEdge(min1, min2)
        
        return nsuccess > 0            
    
                
    def _getNextPair(self):
        """
        this is the function which attempts to find a clever pair of minima to try to 
        connect with the ultimate goal of connecting minstart and minend
        
        this method can be described as follows:
        
        make a new graph Gnew which is complete (all vetices connected).  The edges
        have a weight given by
        
        if self.graph.areConnected(u,v):
            weight(u,v) = 0.
        else:
            weight(u,v) = mindist(u,v)
        
        if an NEB has been attempted between u and v then the edge is removed.
        
        we then find the shortest path between minstart and minend.  We return
        the pair in this path which has edge weight with the smallest non zero value 
        
        update: find the shortest path weighted by distance squared.  This penalizes finding
        the NEB between minima that are very far away.  (Does this too much favor long paths?)
        """
        print "finding a good pair to try to connect"
        #get the shortest path on dist_graph between minstart and minend
        if True:
            print "Gdist has", self.dist_graph.Gdist.number_of_nodes(), "nodes and", self.dist_graph.Gdist.number_of_edges(), "edges"
        path, weights = self.dist_graph.shortestPath(self.minstart, self.minend)
        weightsum = sum(weights)
        if path is None or weightsum >= 10e9:
            print "Can't find any way to try to connect the minima"
            return None, None
        
        #get the weights of the path segements
        weightlist = []
        for i in range(1,len(path)):
            min1 = path[i-1]
            min2 = path[i]
#            w = weights.get((min1,min2))
#            if w is None:
#                w = weights.get((min2,min1))
            w = weights[i-1]
            weightlist.append( (w, min1, min2) )
        
        if True:
            #print the path
            print "best guess for path.  (dist=0.0 means the path is known)"
            for w, min1, min2 in weightlist:
                if w > 1e-6:
                    dist = self.getDist(min1, min2)
                else:
                    dist = w
                print "    path guess", min1._id, min2._id, dist

        #select which minima pair to return
        if self.longest_first:
            weightlist.sort()
            w, min1, min2 = weightlist[-1]
        else:
            weightlist.sort()
            for w, min1, min2 in weightlist:
                if w > 1e-6:
                    break
        return min1, min2
            
        
#        #find the shortest single edge in that path and use that
#        #also, print the path
#        #as the minima pair to try to connect.
#        weightmin = 1e100
#        minpair = (None, None)
#        for i in range(1,len(path)):
#            min1 = path[i-1]
#            min2 = path[i]
#            w = weights.get((min1,min2))
#            if w is None:
#                w = weights.get((min2,min1))
#            #get the distance between min1 and min2. leave as 0. if they are
#            #already connected by transition states
#            dist = w
#            if w > 1e-6:
#                dist = self.getDist(min1, min2)
#            print "    path guess", min1._id, min2._id, dist
#            if w > 1e-10 and w < weightmin:
#                weightmin = w
#                minpair = (min1, min2)
#        return minpair
                
    
    def connect(self, maxiter=200):
        """
        the main loop of the algorithm
        """
        self.NEBattempts = 2;
        for i in range(maxiter):
            self.dist_graph.updateDatabase()
            if self.graph.areConnected(self.minstart, self.minend):
                self.dist_graph.updateDatabase(force=True)
                print "found connection!"
                return
            
            print ""
            print "======== starting connect cycle", i, "========"
            min1, min2 = self._getNextPair()
            #raw_input("Press Enter to continue:")
            if min1 is None or min2 is None:
                break
            local_success = self._localConnect(min1, min2)
            
            if True and i % 10 == 0:
                #do some santy checks
                self.dist_graph.checkGraph()



            
        print "failed to find connection between", self.minstart._id, self.minend._id

    def returnPath(self):
        """return information about the path"""
        if not self.graph.areConnected(self.minstart, self.minend):
            return
        minima = nx.shortest_path(self.graph.graph, self.minstart, self.minend)
        transition_states = []
        mints = [minima[0]]
        for i in range(1,len(minima)):
            m1 = minima[i-1]
            m2 = minima[i]
            ts = self.database.getTransitionState(m1, m2)
            transition_states.append(ts)
            mints.append(ts)
            mints.append(m2)
        
        S = np.zeros(len(mints))
        for i in range(1,len(mints)):
            coords1 = mints[i-1].coords
            coords2 = mints[i].coords
            dist, c1, c2 = self.mindist(coords1, coords2)
            S[i] = S[i-1] + dist
        energies = np.array([m.energy for m in mints])
        return mints, S, energies
        


###########################################################
#only testing stuff below here
###########################################################

def getSetOfMinLJ(natoms = 32): #for testing purposes
    from pygmin.potentials.lj import LJ
    pot = LJ()
    coords = np.random.uniform(-1,1,natoms*3)
    from pygmin.basinhopping import BasinHopping
    from pygmin.takestep.displace import RandomDisplacement
    from pygmin.takestep.adaptive import AdaptiveStepsize
    from pygmin.storage.database import Database
    import os
    #dbfile = "test.db"
    #os.remove(dbfile)
    #saveit = Database(db=dbfile)
    saveit = Database()
    takestep1 = RandomDisplacement()
    takestep = AdaptiveStepsize(takestep1, frequency=15)
    bh = BasinHopping(coords, pot, takestep, storage=saveit.minimum_adder(), outstream=None)
    bh.run(100)
    return pot, saveit


def test(Connect=DoubleEndedConnect, natoms=16):
    from pygmin.landscape import Graph
    from pygmin.optimize.quench import lbfgs_py as quench
    from pygmin.mindist import minPermDistStochastic, MinDistWrapper
    from pygmin.storage.database import Database
    import pygmin.defaults as defaults
    defaults.quenchParams = {"iprint": 1}
    #get min1
    pot, database = getSetOfMinLJ(natoms)
#    from pygmin.potentials.lj import LJ
#    pot = LJ()
#    saveit = Database(db="test.db")
    minima = database.minima()
    min1 = minima[0]
    min2 = minima[1]
    print min1.energy, min2.energy
    
    mindist = MinDistWrapper(minPermDistStochastic, permlist=[range(natoms)], niter=10)
    
    if False:
        #test to see if min1 and min2 are already connected
        connected = graph.areConnected(min1, min2)
        print "at start are minima connected?", connected
        return
 
    connect = Connect(min1, min2, pot, mindist, database)
    connect.connect()
    
    graph = connect.graph
    if False:
        print graph
        for node in graph.graph.nodes():
            print node._id, node.energy
    for ts in graph.storage.transition_states():
        print ts.minimum1._id,ts.minimum2._id, "E", ts.minimum1.energy, ts.minimum2.energy, ts.energy
        
    ret = graph.getPath(min1, min2)
    if ret is None:
        print "no path found"
        return
    distances, path = ret
    with open("path.out", "w") as fout:
        for i in range(len(path)-1):
            m1 = path[i]
            m2 = path[i+1]
            n1 = m1._id
            m2 = m2._id
#            ts = graph._getTS(n1, n2)
#            print "path", n1, "->", n2, m1.E, "/->", ts.E, "\->", m2.E
            fout.write("%f\n" % m1.energy)
            fout.write("%f\n" % ts.energy)
        m2 = path[-1]
        n2 = m2._id
        fout.write("%f\n" % m2.energy)


if __name__ == "__main__":
    test(natoms=38)


    
