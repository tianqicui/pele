#include "pele/rotations.h"
#include "pele/aatopology.h"
#include "pele/vecn.h"

namespace pele{

pele::Array<double>
pele::RigidFragment::to_atomistic(pele::Array<double> const com,
        pele::VecN<3> const & p)
{
    assert(com.size() == _ndim);
    assert(p.size() == 3);
    auto rmat = pele::aa_to_rot_mat(p);
    Array<double> pos(_atom_positions.size());
    HackyMatrix<double> mpos(pos, _ndim);

    // in python this is:
    //      return com + np.dot(R, np.transpose(self.atom_positions)).transpose()
    for (size_t atom = 0; atom<_natoms; ++atom) {
        for (size_t j = 0; j<_ndim; ++j) {
            double val = com[j];
            for (size_t k = 0; k<_ndim; ++k) {
                val += rmat(j,k) * _atom_positions_matrix(atom,k);
            }
            mpos(atom, j) = val;
        }
    }
    return pos;
}

void
pele::RigidFragment::transform_grad(
        pele::VecN<3> const & p,
        pele::Array<double> const g,
        pele::VecN<3> & g_com,
        pele::VecN<3> & g_rot
        )
{
    assert(g.size() == natoms() * 3);
    // view the array as a matrix
    HackyMatrix<double> gmat(g, 3);

    // compute the rotation matrix and derivatives
    pele::MatrixNM<3,3> rmat;
    pele::MatrixNM<3,3> drm1;
    pele::MatrixNM<3,3> drm2;
    pele::MatrixNM<3,3> drm3;
    rot_mat_derivatives(p, rmat, drm1, drm2, drm3);

    // do the center of mass coordinates
    for (size_t k=0; k<3; ++k) {
        double val = 0;
        for (size_t atom=0; atom < _natoms; ++atom) {
            val += gmat(atom,k);
        }
        g_com[k] = val;
    }

    // now do the rotations
    g_rot.assign(0);
    for (size_t atom=0; atom < _natoms; ++atom) {
        double val1 = 0;
        double val2 = 0;
        double val3 = 0;
        for (size_t i=0; i<3; ++i) {
            for (size_t j=0; j<3; ++j) {
                val1 += gmat(atom,i) * drm1(i,j) * _atom_positions_matrix(atom,j);
                val2 += gmat(atom,i) * drm2(i,j) * _atom_positions_matrix(atom,j);
                val3 += gmat(atom,i) * drm3(i,j) * _atom_positions_matrix(atom,j);
            }
        }
        g_rot[0] += val1;
        g_rot[1] += val2;
        g_rot[2] += val3;
    }
}

Array<double>
pele::RBTopology::to_atomistic(Array<double> rbcoords)
{
    if (natoms_total() == 0) {
        finalize();
    }
    if ( rbcoords.size() != nrigid() * 6 ) {
        throw std::invalid_argument("rbcoords has the wrong size");
    }

    size_t const nrigid = _sites.size();
    CoordsAdaptor ca(nrigid, 0, rbcoords);
    auto rb_pos = ca.get_rb_positions();
    auto rb_rot = ca.get_rb_rotations();
    Array<double> atomistic(3 * natoms_total());
    // view the atomistic coords as a matrix
    HackyMatrix<double> atomistic_mat(atomistic, 3);
    size_t istart = 0;
    for (size_t isite=0; isite<nrigid; ++isite) {
        VecN<3> psite = rb_rot.view(isite*3, isite*3+3);
        auto site_atom_positions = _sites[isite].to_atomistic(
                rb_pos.view(isite*3, isite*3+3),
                psite
                );
        Array<double> atomistic_view(atomistic.view(istart, istart + site_atom_positions.size()));
        atomistic_view.assign(site_atom_positions);

        istart += site_atom_positions.size();
    }
    assert(istart == natoms_total() * 3);
    return atomistic;
}

void
pele::RBTopology::transform_gradient(pele::Array<double> rbcoords,
        pele::Array<double> grad, pele::Array<double> rbgrad)
{
    if (natoms_total() == 0) {
        finalize();
    }
    if ( rbcoords.size() != nrigid() * 6 ) {
        throw std::invalid_argument("rbcoords has the wrong size");
    }
    if (grad.size() != natoms_total() * 3) {
        throw std::invalid_argument("grad has the wrong size");
    }
    if (rbgrad.size() != rbcoords.size()) {
        throw std::invalid_argument("rbgrad has the wrong size");
    }

    CoordsAdaptor ca(nrigid(), 0, rbcoords);
    pele::Array<double> coords_rot(ca.get_rb_rotations());
//        pele::Array<double> rbgrad(rbcoords.size());
    CoordsAdaptor rbgrad_ca(nrigid(), 0, rbgrad);
    HackyMatrix<double> g_com(rbgrad_ca.get_rb_positions(), 3);
    HackyMatrix<double> g_rot(rbgrad_ca.get_rb_rotations(), 3);

    size_t istart = 0;
    for (size_t isite=0; isite<nrigid(); ++isite) {
        size_t const site_ndof = _sites[isite].natoms() * 3;
//            std::cout << grad.size() << " " << istart << " " << site_ndof << " " << istart + site_ndof << "\n";
        Array<double> g_site     = grad.view      (istart, istart + site_ndof);
        Array<double> p          = coords_rot.view(isite*3, isite*3 + 3);
        Array<double> g_com_site = g_com.view     (isite*3, isite*3 + 3);
        Array<double> g_rot_site = g_rot.view     (isite*3, isite*3 + 3);
        _sites[isite].transform_grad(p, g_site, g_com_site, g_rot_site);
        istart += site_ndof;
    }
}

pele::VecN<3>
pele::RBTopology::align_angle_axis_vectors(pele::VecN<3> const & p1,
        pele::VecN<3> const & p2in)
{
    pele::VecN<3> p2 = p2in;
    pele::VecN<3> n2, p2n;
    if (norm<3>(p2) < 1e-6) {
        if (norm<3>(p1) < 1e-6) {
            return p2;
        }
        n2 = p1;
        n2 *= 2. * M_PI / norm<3>(p1);
    } else {
        n2 = p2;
        n2 *= 2. * M_PI / norm<3>(p2);
    }

    while (true) {
        p2n = p2;
        p2n += n2;
        if (norm<3>(p2n - p1) > norm<3>(p2 - p1)) {
            break;
        }
        p2 = p2n;
    }

    while (true) {
        p2n = p2;
        p2n -= n2;
        if (norm<3>(p2n - p1) > norm<3>(p2 - p1)) {
            break;
        }
        p2 = p2n;
    }
    return p2;
}

void
pele::RBTopology::align_all_angle_axis_vectors(pele::Array<double> x1,
        pele::Array<double> x2)
{
    auto c1 = get_coords_adaptor(x1);
    auto c2 = get_coords_adaptor(x2);
    for (size_t isite = 0; isite < nrigid(); ++isite) {
        VecN<3> p1 = c1.get_rb_rotation(isite);
        pele::Array<double> p2 = c2.get_rb_rotation(isite);
        auto p2new = align_angle_axis_vectors(p1, p2);
        std::copy(p2new.begin(), p2new.end(), p2.begin());
    }
}

void
pele::RBTopology::align_path(std::list<pele::Array<double> > path)
{
    auto iter1 = path.begin();
    auto iter2 = path.begin();
    iter2++;
    while (iter2 != path.end()) {
        align_all_angle_axis_vectors(*iter1, *iter2);
        ++iter1;
        ++iter2;
    }
}

void
pele::TransformAACluster::rotate(pele::Array<double> x,
        pele::MatrixNM<3,3> const & mx)
{
    auto ca = m_topology->get_coords_adaptor(x);
    if(m_topology->nrigid() > 0) {
        // rotate the center of mass positions by mx
        pele::HackyMatrix<double> rb_pos(ca.get_rb_positions(), 3);
        // make a HackyMatrix view of the transposed rotation matrix
        auto mxT = pele::transpose(mx);
        pele::HackyMatrix<double> mxT_view(mxT.data(), 3, 3);
        assert(mxT_view(0,1) == mx(1,0));
        // do the multiplication
        auto result = hacky_mat_mul(rb_pos, mxT_view);
        // copy the results back into the coordinates array
//        std::cout << "result " << result << std::endl;
        rb_pos.assign(result);

        // rotate each aa rotation by mx
        VecN<3> dp = pele::rot_mat_to_aa(mx);
        auto rb_rot = ca.get_rb_rotations();
        for (size_t isite = 0; isite < m_topology->nrigid(); ++isite) {
            pele::Array<double> pview = rb_rot.view(isite*3, isite*3+3);
            VecN<3> p = pele::rotate_aa(pview, dp);
            // copy the vector back into pview
            std::copy(p.begin(), p.end(), pview.begin());
        }
    }
    if (m_topology->number_of_non_rigid_atoms() > 0) {
        throw std::runtime_error("non-rigid atoms is not yet supported");
//            ca.posAtom[:] = np.dot(mx, ca.posAtom.transpose()).transpose()
    }
}

} // namespace pele
