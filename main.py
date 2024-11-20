from calendar import Calendar

import conexionserver
from venAux import *
import conexion
import eventos
import style
from ventPrincipal import *
import sys
import var
import clientes
import propiedades

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_ventPrincipal()
        var.ui.setupUi(self)
        var.uicalendar= Calendar()
        var.dlggestion = dlgGestionProp()
        var.dlgabrir = FileDialogAbrir()
        var.dlgabout = dlgAbout()
        var.historico = 1
        self.setStyleSheet(style.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        #conexionserver.ConexionServer.crear_conexion(self)
        clientes.Clientes.cargaTablaClientes(self)
        propiedades.Propiedades.cargaTablaPropiedades(self)



        '''
        Zona de eventos de la tabla
        '''
        eventos.Eventos.resizeTablaClientes(self)
        var.ui.tablaClientes.clicked.connect(clientes.Clientes.cargaOneCliente)
        eventos.Eventos.resizeTablaPropiedades(self)
        var.ui.tablaProp.clicked.connect(propiedades.Propiedades.cargaOnePropiedad)

        '''
        Zona de eventos del menuBar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_BackUp.triggered.connect(eventos.Eventos.crearBackUp)
        var.ui.actionRestaurar_BackUp.triggered.connect(eventos.Eventos.restaurarBackUp)
        var.ui.actionTipoPropiedad.triggered.connect(eventos.Eventos.abrirTipoProp)
        var.ui.actionAbout.triggered.connect(eventos.Eventos.abrirAbout)
        var.ui.actionbarBuscar.triggered.connect(propiedades.Propiedades.filtrarProp)
        var.ui.actionbarGestionProp.triggered.connect(eventos.Eventos.abrirTipoProp)
        var.ui.actionbarGestionProp.triggered.connect(eventos.Eventos.abrirTipoProp)


        '''
        Zona de eventos de los botones
        '''

        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnModifiCli.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnDelCli.clicked.connect(clientes.Clientes.bajaCliente)
        var.ui.btnAltaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0, 0))
        var.ui.btnBajaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0, 1))
        var.ui.btnFechaAltaProp.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1, 0))
        var.ui.btnFechaBajaProp.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1, 1))
        var.ui.btnGrabarProp.clicked.connect(propiedades.Propiedades.altaPropiedad)
        var.ui.btnModifProp.clicked.connect(propiedades.Propiedades.modifPropiedad)
        var.ui.btnDelProp.clicked.connect(propiedades.Propiedades.bajaPropiedad)
        var.ui.btnBuscarTipoProp.clicked.connect(propiedades.Propiedades.cargaTablaPropiedades)
        var.ui.btnBuscarCli.clicked.connect(clientes.Clientes.cargaTablaClientes)




        '''
        Zona de eventos de las cajas de texto
        '''

        var.ui.txtDniCli.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDniCli.text()))
        var.ui.txtEmailCli.editingFinished.connect(lambda: clientes.Clientes.checkEmail(var.ui.txtEmailCli.text()))
        var.ui.txtMovilCli.editingFinished.connect(lambda: clientes.Clientes.checktelefono(var.ui.txtMovilCli.text()))
        var.ui.txtPrecioVProp.textChanged.connect(lambda: propiedades.Propiedades.manageChkBox(self))
        var.ui.txtPrecioAProp.textChanged.connect(lambda: propiedades.Propiedades.manageChkBox(self))
        var.ui.txtFechaBajaProp.textChanged.connect(lambda: propiedades.Propiedades.manageRadioButtons(self))



        '''
        Zona de eventos de los comboBox
        
        '''
        eventos.Eventos.cargarProvincias(self)
        eventos.Eventos.cargarMunicipios(self)
        var.ui.cmbProCli.currentIndexChanged.connect(eventos.Eventos.cargarMunicipios)
        eventos.Eventos.cargarProvinciasProp(self)
        eventos.Eventos.cargarMunicipiosProp(self)
        var.ui.cmbProvProp.currentIndexChanged.connect(eventos.Eventos.cargarMunicipiosProp)
        eventos.Eventos.cargarTipoProp(self)

        '''
            Zona de eventos del toolBar
        '''

        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbar_limpiar.triggered.connect(eventos.Eventos.limpiarPanel)
        var.ui.actionExportar_Clientes_CSV.triggered.connect(eventos.Eventos.exportCSVClientes)
        var.ui.actionExportar_Clientes_JSON.triggered.connect(eventos.Eventos.exportJSONClientes)
        var.ui.actionExportar_Propiedades_CSV.triggered.connect(eventos.Eventos.exportCSVProp)
        var.ui.actionExportar_Propiedades_JSON.triggered.connect(eventos.Eventos.exportJSONProp)


        '''
        Zona de eventos de los checkbox
        '''
        var.ui.chkHistoriaCli.stateChanged.connect(clientes.Clientes.historicoCli)
        var.ui.chkHistoriaProp.stateChanged.connect(propiedades.Propiedades.cargaTablaPropiedades)
        propiedades.Propiedades.manageChkBox(self)

        '''
        Zona de eventos de los RdioButtons
        '''

        propiedades.Propiedades.manageRadioButtons(self)




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())
