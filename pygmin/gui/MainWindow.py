# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Wed Apr 24 20:40:55 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(839, 623)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.BHTab = QtGui.QWidget()
        self.BHTab.setObjectName(_fromUtf8("BHTab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.BHTab)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.ogl_main = Show3D(self.BHTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ogl_main.sizePolicy().hasHeightForWidth())
        self.ogl_main.setSizePolicy(sizePolicy)
        self.ogl_main.setObjectName(_fromUtf8("ogl_main"))
        self.horizontalLayout_3.addWidget(self.ogl_main)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_2 = QtGui.QLabel(self.BHTab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_3.addWidget(self.label_2)
        self.list_minima_main = QtGui.QListView(self.BHTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_minima_main.sizePolicy().hasHeightForWidth())
        self.list_minima_main.setSizePolicy(sizePolicy)
        self.list_minima_main.setMaximumSize(QtCore.QSize(200, 16777215))
        self.list_minima_main.setObjectName(_fromUtf8("list_minima_main"))
        self.verticalLayout_3.addWidget(self.list_minima_main)
        self.pushTakestepExplorer = QtGui.QPushButton(self.BHTab)
        self.pushTakestepExplorer.setObjectName(_fromUtf8("pushTakestepExplorer"))
        self.verticalLayout_3.addWidget(self.pushTakestepExplorer)
        self.pushNormalmodesMin = QtGui.QPushButton(self.BHTab)
        self.pushNormalmodesMin.setObjectName(_fromUtf8("pushNormalmodesMin"))
        self.verticalLayout_3.addWidget(self.pushNormalmodesMin)
        self.btn_start_basinhopping = QtGui.QPushButton(self.BHTab)
        self.btn_start_basinhopping.setObjectName(_fromUtf8("btn_start_basinhopping"))
        self.verticalLayout_3.addWidget(self.btn_start_basinhopping)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.BHTab, _fromUtf8(""))
        self.NEBTab = QtGui.QWidget()
        self.NEBTab.setObjectName(_fromUtf8("NEBTab"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.NEBTab)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(5, -1, -1, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.oglPath = Show3DWithSlider(self.NEBTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.oglPath.sizePolicy().hasHeightForWidth())
        self.oglPath.setSizePolicy(sizePolicy)
        self.oglPath.setObjectName(_fromUtf8("oglPath"))
        self.verticalLayout.addWidget(self.oglPath)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(6, -1, -1, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.listMinima1 = QtGui.QListView(self.NEBTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listMinima1.sizePolicy().hasHeightForWidth())
        self.listMinima1.setSizePolicy(sizePolicy)
        self.listMinima1.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listMinima1.setObjectName(_fromUtf8("listMinima1"))
        self.verticalLayout_5.addWidget(self.listMinima1)
        self.listMinima2 = QtGui.QListView(self.NEBTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listMinima2.sizePolicy().hasHeightForWidth())
        self.listMinima2.setSizePolicy(sizePolicy)
        self.listMinima2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listMinima2.setObjectName(_fromUtf8("listMinima2"))
        self.verticalLayout_5.addWidget(self.listMinima2)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setContentsMargins(20, 0, 20, -1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btnAlign = QtGui.QPushButton(self.NEBTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAlign.sizePolicy().hasHeightForWidth())
        self.btnAlign.setSizePolicy(sizePolicy)
        self.btnAlign.setMaximumSize(QtCore.QSize(100, 100))
        self.btnAlign.setObjectName(_fromUtf8("btnAlign"))
        self.gridLayout_2.addWidget(self.btnAlign, 1, 0, 1, 1)
        self.btnReconnect = QtGui.QPushButton(self.NEBTab)
        self.btnReconnect.setObjectName(_fromUtf8("btnReconnect"))
        self.gridLayout_2.addWidget(self.btnReconnect, 3, 1, 1, 1)
        self.btnNEB = QtGui.QPushButton(self.NEBTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnNEB.sizePolicy().hasHeightForWidth())
        self.btnNEB.setSizePolicy(sizePolicy)
        self.btnNEB.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btnNEB.setObjectName(_fromUtf8("btnNEB"))
        self.gridLayout_2.addWidget(self.btnNEB, 2, 0, 1, 1)
        self.btnConnect = QtGui.QPushButton(self.NEBTab)
        self.btnConnect.setObjectName(_fromUtf8("btnConnect"))
        self.gridLayout_2.addWidget(self.btnConnect, 3, 0, 1, 1)
        self.btnShowGraph = QtGui.QPushButton(self.NEBTab)
        self.btnShowGraph.setObjectName(_fromUtf8("btnShowGraph"))
        self.gridLayout_2.addWidget(self.btnShowGraph, 5, 0, 1, 1)
        self.btnDisconnectivity_graph = QtGui.QPushButton(self.NEBTab)
        self.btnDisconnectivity_graph.setObjectName(_fromUtf8("btnDisconnectivity_graph"))
        self.gridLayout_2.addWidget(self.btnDisconnectivity_graph, 5, 1, 1, 1)
        self.btn_connect_in_optim = QtGui.QPushButton(self.NEBTab)
        self.btn_connect_in_optim.setObjectName(_fromUtf8("btn_connect_in_optim"))
        self.gridLayout_2.addWidget(self.btn_connect_in_optim, 4, 1, 1, 1)
        self.btn_connect_all = QtGui.QPushButton(self.NEBTab)
        self.btn_connect_all.setObjectName(_fromUtf8("btn_connect_all"))
        self.gridLayout_2.addWidget(self.btn_connect_all, 4, 0, 1, 1)
        self.btn_close_all = QtGui.QPushButton(self.NEBTab)
        self.btn_close_all.setObjectName(_fromUtf8("btn_close_all"))
        self.gridLayout_2.addWidget(self.btn_close_all, 1, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.tabWidget.addTab(self.NEBTab, _fromUtf8(""))
        self.TSTab = QtGui.QWidget()
        self.TSTab.setObjectName(_fromUtf8("TSTab"))
        self.gridLayout_8 = QtGui.QGridLayout(self.TSTab)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.oglTS = Show3DWithSlider(self.TSTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.oglTS.sizePolicy().hasHeightForWidth())
        self.oglTS.setSizePolicy(sizePolicy)
        self.oglTS.setObjectName(_fromUtf8("oglTS"))
        self.gridLayout_8.addWidget(self.oglTS, 0, 0, 1, 1)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.list_TS = QtGui.QListWidget(self.TSTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_TS.sizePolicy().hasHeightForWidth())
        self.list_TS.setSizePolicy(sizePolicy)
        self.list_TS.setMaximumSize(QtCore.QSize(200, 16777215))
        self.list_TS.setObjectName(_fromUtf8("list_TS"))
        self.verticalLayout_9.addWidget(self.list_TS)
        self.pushNormalmodesTS = QtGui.QPushButton(self.TSTab)
        self.pushNormalmodesTS.setObjectName(_fromUtf8("pushNormalmodesTS"))
        self.verticalLayout_9.addWidget(self.pushNormalmodesTS)
        self.gridLayout_8.addLayout(self.verticalLayout_9, 0, 2, 1, 1)
        self.tabWidget.addTab(self.TSTab, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 839, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuSimulation = QtGui.QMenu(self.menubar)
        self.menuSimulation.setObjectName(_fromUtf8("menuSimulation"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuActions = QtGui.QMenu(self.menubar)
        self.menuActions.setObjectName(_fromUtf8("menuActions"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionClear = QtGui.QAction(MainWindow)
        self.actionClear.setObjectName(_fromUtf8("actionClear"))
        self.action_db_connect = QtGui.QAction(MainWindow)
        self.action_db_connect.setObjectName(_fromUtf8("action_db_connect"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.action_delete_minimum = QtGui.QAction(MainWindow)
        self.action_delete_minimum.setObjectName(_fromUtf8("action_delete_minimum"))
        self.action_edit_params = QtGui.QAction(MainWindow)
        self.action_edit_params.setObjectName(_fromUtf8("action_edit_params"))
        self.action_merge_minima = QtGui.QAction(MainWindow)
        self.action_merge_minima.setObjectName(_fromUtf8("action_merge_minima"))
        self.menuSimulation.addAction(self.action_db_connect)
        self.menuHelp.addAction(self.actionAbout)
        self.menuActions.addAction(self.action_delete_minimum)
        self.menuActions.addAction(self.action_merge_minima)
        self.menuActions.addAction(self.action_edit_params)
        self.menubar.addAction(self.menuSimulation.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuActions.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_2.setText(_translate("MainWindow", "Energy (id)", None))
        self.pushTakestepExplorer.setText(_translate("MainWindow", "Takestep explorer", None))
        self.pushNormalmodesMin.setText(_translate("MainWindow", "Normalmodes", None))
        self.btn_start_basinhopping.setToolTip(_translate("MainWindow", "<html><head/><body><p>Start a short basinhopping run</p></body></html>", None))
        self.btn_start_basinhopping.setText(_translate("MainWindow", "Run", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.BHTab), _translate("MainWindow", "Basin Hopping", None))
        self.btnAlign.setToolTip(_translate("MainWindow", "<html><head/><body><p>Find best alignment between two structures</p></body></html>", None))
        self.btnAlign.setText(_translate("MainWindow", "Align", None))
        self.btnReconnect.setToolTip(_translate("MainWindow", "<html><head/><body><p>Start a fresh double ended connect run</p></body></html>", None))
        self.btnReconnect.setText(_translate("MainWindow", "Reconnect", None))
        self.btnNEB.setToolTip(_translate("MainWindow", "<html><head/><body><p>Start an NEB run (no alignment is done)</p></body></html>", None))
        self.btnNEB.setText(_translate("MainWindow", "NEB", None))
        self.btnConnect.setToolTip(_translate("MainWindow", "<html><head/><body><p>Start a double ended connect run</p></body></html>", None))
        self.btnConnect.setText(_translate("MainWindow", "Connect", None))
        self.btnShowGraph.setToolTip(_translate("MainWindow", "<html><head/><body><p>Show the graph of minima and transition states</p></body></html>", None))
        self.btnShowGraph.setText(_translate("MainWindow", "show graph", None))
        self.btnDisconnectivity_graph.setToolTip(_translate("MainWindow", "<html><head/><body><p>Show the disconnectivity graph</p></body></html>", None))
        self.btnDisconnectivity_graph.setText(_translate("MainWindow", "disconnectivity graph", None))
        self.btn_connect_in_optim.setToolTip(_translate("MainWindow", "<html><head/><body><p>Spawn an external OPTIM job</p></body></html>", None))
        self.btn_connect_in_optim.setText(_translate("MainWindow", "Connect in OPTIM", None))
        self.btn_connect_all.setText(_translate("MainWindow", "Connect All", None))
        self.btn_close_all.setText(_translate("MainWindow", "Close Windows", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.NEBTab), _translate("MainWindow", "Connect", None))
        self.pushNormalmodesTS.setText(_translate("MainWindow", "Normalmodes", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TSTab), _translate("MainWindow", "Transition States", None))
        self.menuSimulation.setTitle(_translate("MainWindow", "Database", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.menuActions.setTitle(_translate("MainWindow", "Actions", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionClear.setText(_translate("MainWindow", "Clear Database", None))
        self.action_db_connect.setText(_translate("MainWindow", "Connect to Database", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.action_delete_minimum.setText(_translate("MainWindow", "Delete Minimum", None))
        self.action_edit_params.setText(_translate("MainWindow", "Edit default parameters", None))
        self.action_merge_minima.setText(_translate("MainWindow", "Merge Minima", None))

from show3d_with_slider import Show3DWithSlider
from pygmin.gui.show3d import Show3D
