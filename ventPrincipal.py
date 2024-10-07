# Form implementation generated from reading ui file '.\\templates\\ventPrincipal.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ventPrincipal(object):
    def setupUi(self, ventPrincipal):
        ventPrincipal.setObjectName("ventPrincipal")
        ventPrincipal.resize(1161, 768)
        ventPrincipal.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\\\templates\\../img/logo.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ventPrincipal.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(parent=ventPrincipal)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 3, 1, 1)
        self.panPrincipal = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.panPrincipal.setStyleSheet("")
        self.panPrincipal.setObjectName("panPrincipal")
        self.PesClientes = QtWidgets.QWidget()
        self.PesClientes.setObjectName("PesClientes")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.PesClientes)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lblMuniCli = QtWidgets.QLabel(parent=self.PesClientes)
        self.lblMuniCli.setObjectName("lblMuniCli")
        self.gridLayout.addWidget(self.lblMuniCli, 3, 10, 1, 1)
        self.txtMovilCli = QtWidgets.QLineEdit(parent=self.PesClientes)
        self.txtMovilCli.setMinimumSize(QtCore.QSize(150, 0))
        self.txtMovilCli.setMaximumSize(QtCore.QSize(150, 16777215))
        self.txtMovilCli.setObjectName("txtMovilCli")
        self.gridLayout.addWidget(self.txtMovilCli, 2, 5, 1, 4)
        self.txtDNomCli = QtWidgets.QLineEdit(parent=self.PesClientes)
        self.txtDNomCli.setMinimumSize(QtCore.QSize(200, 0))
        self.txtDNomCli.setMaximumSize(QtCore.QSize(200, 16777215))
        self.txtDNomCli.setObjectName("txtDNomCli")
        self.gridLayout.addWidget(self.txtDNomCli, 1, 5, 1, 7)
        self.lblEmailCli = QtWidgets.QLabel(parent=self.PesClientes)
        self.lblEmailCli.setObjectName("lblEmailCli")
        self.gridLayout.addWidget(self.lblEmailCli, 2, 1, 1, 1)
        self.txtEmailCli = QtWidgets.QLineEdit(parent=self.PesClientes)
        self.txtEmailCli.setMinimumSize(QtCore.QSize(300, 0))
        self.txtEmailCli.setMaximumSize(QtCore.QSize(450, 16777215))
        self.txtEmailCli.setObjectName("txtEmailCli")
        self.gridLayout.addWidget(self.txtEmailCli, 2, 2, 1, 1)
        self.cmbProCli = QtWidgets.QComboBox(parent=self.PesClientes)
        self.cmbProCli.setMinimumSize(QtCore.QSize(120, 0))
        self.cmbProCli.setMaximumSize(QtCore.QSize(120, 16777215))
        self.cmbProCli.setObjectName("cmbProCli")
        self.gridLayout.addWidget(self.cmbProCli, 3, 8, 1, 1)
        self.cmbMuniCli = QtWidgets.QComboBox(parent=self.PesClientes)
        self.cmbMuniCli.setMinimumSize(QtCore.QSize(200, 0))
        self.cmbMuniCli.setObjectName("cmbMuniCli")
        self.gridLayout.addWidget(self.cmbMuniCli, 3, 11, 1, 2)
        self.chkHistoriaCli = QtWidgets.QCheckBox(parent=self.PesClientes)
        self.chkHistoriaCli.setObjectName("chkHistoriaCli")
        self.gridLayout.addWidget(self.chkHistoriaCli, 1, 12, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 9, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 3, 1, 1)
        self.lblDniCli = QtWidgets.QLabel(parent=self.PesClientes)
        self.lblDniCli.setObjectName("lblDniCli")
        self.gridLayout.addWidget(self.lblDniCli, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem4, 1, 3, 1, 1)
        self.txtDniCli = QtWidgets.QLineEdit(parent=self.PesClientes)
        self.txtDniCli.setMinimumSize(QtCore.QSize(120, 0))
        self.txtDniCli.setMaximumSize(QtCore.QSize(120, 16777215))
        self.txtDniCli.setStyleSheet("background-color: rgb(251, 255, 205);")
        self.txtDniCli.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.txtDniCli.setObjectName("txtDniCli")
        self.gridLayout.addWidget(self.txtDniCli, 0, 2, 1, 1)
        self.txtApelCli = QtWidgets.QLineEdit(parent=self.PesClientes)
        self.txtApelCli.setMinimumSize(QtCore.QSize(300, 0))
        self.txtApelCli.setMaximumSize(QtCore.QSize(450, 16777215))
        self.txtApelCli.setStyleSheet("background-color: rgb(250, 255, 203);")
        self.txtApelCli.setObjectName("txtApelCli")
        self.gridLayout.addWidget(self.txtApelCli, 1, 2, 1, 1)
        self.lblApelCli = QtWidgets.QLabel(parent=self.PesClientes)
        self.lblApelCli.setObjectName("lblApelCli")
        self.gridLayout.addWidget(self.lblApelCli, 1, 1, 1, 1)
        self.lblDirCLi = QtWidgets.QLabel(parent=self.PesClientes)
        self.lblDirCLi.setObjectName("lblDirCLi")
        self.gridLayout.addWidget(self.lblDirCLi, 3, 1, 1, 1)
        self.txtDirCli = QtWidgets.QLineEdit(parent=self.PesClientes)
        self.txtDirCli.setMinimumSize(QtCore.QSize(360, 0))
        self.txtDirCli.setMaximumSize(QtCore.QSize(1200, 16777215))
        self.txtDirCli.setObjectName("txtDirCli")
        self.gridLayout.addWidget(self.txtDirCli, 3, 2, 1, 4)
        self.lblProCli = QtWidgets.QLabel(parent=self.PesClientes)
        self.lblProCli.setObjectName("lblProCli")
        self.gridLayout.addWidget(self.lblProCli, 3, 7, 1, 1)
        self.lblMovilCli = QtWidgets.QLabel(parent=self.PesClientes)
        self.lblMovilCli.setObjectName("lblMovilCli")
        self.gridLayout.addWidget(self.lblMovilCli, 2, 4, 1, 1)
        self.lblNomCli = QtWidgets.QLabel(parent=self.PesClientes)
        self.lblNomCli.setObjectName("lblNomCli")
        self.gridLayout.addWidget(self.lblNomCli, 1, 4, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem5, 3, 6, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem6, 0, 0, 4, 1)
        spacerItem7 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem7, 0, 13, 4, 1)
        self.txtAltaCli = QtWidgets.QLineEdit(parent=self.PesClientes)
        self.txtAltaCli.setMaximumSize(QtCore.QSize(75, 16777215))
        self.txtAltaCli.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.txtAltaCli.setObjectName("txtAltaCli")
        self.gridLayout.addWidget(self.txtAltaCli, 0, 5, 1, 1)
        self.lblAltaCli = QtWidgets.QLabel(parent=self.PesClientes)
        self.lblAltaCli.setObjectName("lblAltaCli")
        self.gridLayout.addWidget(self.lblAltaCli, 0, 4, 1, 1)
        self.btnAltaCli = QtWidgets.QPushButton(parent=self.PesClientes)
        self.btnAltaCli.setMinimumSize(QtCore.QSize(32, 32))
        self.btnAltaCli.setMaximumSize(QtCore.QSize(32, 32))
        self.btnAltaCli.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btnAltaCli.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(".\\\\templates\\../img/calendar.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnAltaCli.setIcon(icon1)
        self.btnAltaCli.setIconSize(QtCore.QSize(21, 21))
        self.btnAltaCli.setObjectName("btnAltaCli")
        self.gridLayout.addWidget(self.btnAltaCli, 0, 6, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem8 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem8)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem9 = QtWidgets.QSpacerItem(328, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem9)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnGrabarCli = QtWidgets.QPushButton(parent=self.PesClientes)
        self.btnGrabarCli.setMinimumSize(QtCore.QSize(80, 25))
        self.btnGrabarCli.setMaximumSize(QtCore.QSize(80, 25))
        self.btnGrabarCli.setObjectName("btnGrabarCli")
        self.horizontalLayout.addWidget(self.btnGrabarCli, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.btnModifiCli = QtWidgets.QPushButton(parent=self.PesClientes)
        self.btnModifiCli.setMinimumSize(QtCore.QSize(80, 25))
        self.btnModifiCli.setMaximumSize(QtCore.QSize(80, 25))
        self.btnModifiCli.setObjectName("btnModifiCli")
        self.horizontalLayout.addWidget(self.btnModifiCli, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.btnDelCli = QtWidgets.QPushButton(parent=self.PesClientes)
        self.btnDelCli.setMinimumSize(QtCore.QSize(80, 25))
        self.btnDelCli.setMaximumSize(QtCore.QSize(80, 25))
        self.btnDelCli.setObjectName("btnDelCli")
        self.horizontalLayout.addWidget(self.btnDelCli, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem10 = QtWidgets.QSpacerItem(348, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem10)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(parent=self.PesClientes)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.tablaClientes = QtWidgets.QTableWidget(parent=self.PesClientes)
        self.tablaClientes.setAutoFillBackground(False)
        self.tablaClientes.setObjectName("tablaClientes")
        self.tablaClientes.setColumnCount(0)
        self.tablaClientes.setRowCount(0)
        self.verticalLayout.addWidget(self.tablaClientes)
        self.panPrincipal.addTab(self.PesClientes, "")
        self.PesConstruct = QtWidgets.QWidget()
        self.PesConstruct.setObjectName("PesConstruct")
        self.label = QtWidgets.QLabel(parent=self.PesConstruct)
        self.label.setGeometry(QtCore.QRect(390, 280, 121, 41))
        self.label.setObjectName("label")
        self.panPrincipal.addTab(self.PesConstruct, "")
        self.gridLayout_2.addWidget(self.panPrincipal, 0, 1, 1, 1)
        ventPrincipal.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=ventPrincipal)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1161, 21))
        self.menubar.setObjectName("menubar")
        self.menuSalir = QtWidgets.QMenu(parent=self.menubar)
        self.menuSalir.setObjectName("menuSalir")
        ventPrincipal.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=ventPrincipal)
        self.statusbar.setObjectName("statusbar")
        ventPrincipal.setStatusBar(self.statusbar)
        self.actionSalir = QtGui.QAction(parent=ventPrincipal)
        self.actionSalir.setObjectName("actionSalir")
        self.menuSalir.addAction(self.actionSalir)
        self.menubar.addAction(self.menuSalir.menuAction())

        self.retranslateUi(ventPrincipal)
        self.panPrincipal.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ventPrincipal)

    def retranslateUi(self, ventPrincipal):
        _translate = QtCore.QCoreApplication.translate
        ventPrincipal.setWindowTitle(_translate("ventPrincipal", "InmoTeis"))
        self.lblMuniCli.setText(_translate("ventPrincipal", "Municipio:"))
        self.lblEmailCli.setText(_translate("ventPrincipal", "Email:"))
        self.chkHistoriaCli.setText(_translate("ventPrincipal", "Histórico"))
        self.lblDniCli.setText(_translate("ventPrincipal", "DNI/CIF"))
        self.lblApelCli.setText(_translate("ventPrincipal", "Apellidos:"))
        self.lblDirCLi.setText(_translate("ventPrincipal", "Dirección:"))
        self.lblProCli.setText(_translate("ventPrincipal", "Provincia:"))
        self.lblMovilCli.setText(_translate("ventPrincipal", "Móvil:"))
        self.lblNomCli.setText(_translate("ventPrincipal", "Nombre:"))
        self.lblAltaCli.setText(_translate("ventPrincipal", "Fecha Alta"))
        self.btnGrabarCli.setText(_translate("ventPrincipal", "Grabar"))
        self.btnModifiCli.setText(_translate("ventPrincipal", "Modificar"))
        self.btnDelCli.setText(_translate("ventPrincipal", "Eliminar"))
        self.panPrincipal.setTabText(self.panPrincipal.indexOf(self.PesClientes), _translate("ventPrincipal", "Clientes"))
        self.label.setText(_translate("ventPrincipal", "Panel en construcción"))
        self.panPrincipal.setTabText(self.panPrincipal.indexOf(self.PesConstruct), _translate("ventPrincipal", "Tab 2"))
        self.menuSalir.setTitle(_translate("ventPrincipal", "Archivo"))
        self.actionSalir.setText(_translate("ventPrincipal", "Salir"))
