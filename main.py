from calendar import Calendar

import vendedor
from venAux import *
import conexion
import eventos
import style
from ventPrincipal import *
import sys
import var
import clientes
import propiedades
import informes
import facturas

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        conexion.Conexion.db_conexion(self)
        super(Main, self).__init__()
        var.ui = Ui_ventPrincipal()
        var.ui.setupUi(self)
        var.uicalendar= Calendar()
        var.dlggestion = dlgGestionProp()
        var.dlgabrir = FileDialogAbrir()
        var.dlgabout = dlgAbout()
        var.dlgInforme = dlgInformeProp()
        var.historico = 1
        var.current_page_cli = 0
        var.items_per_page_cli = 15
        var.current_page_prop = 0
        var.items_per_page_prop = 15
        self.setStyleSheet(style.load_stylesheet())
        clientes.Clientes.cargaTablaClientes(self)
        propiedades.Propiedades.cargaTablaPropiedades(self)
        vendedor.Vendedor.cargarTablaVendedores(self)
        facturas.Facturas.cargaTablaFacturas()
        facturas.Facturas.cargaTablaVentas()



        '''
        Zona de eventos de la tabla
        '''
        eventos.Eventos.resizeTablaClientes(self)
        var.ui.tablaClientes.clicked.connect(clientes.Clientes.cargaOneCliente)
        eventos.Eventos.resizeTablaPropiedades(self)
        var.ui.tablaProp.clicked.connect(propiedades.Propiedades.cargaOnePropiedad)
        eventos.Eventos.resizeTablaVendedores(self)
        var.ui.tablaVen.clicked.connect(vendedor.Vendedor.cargarOneVendedor)
        eventos.Eventos.resizeTablaFacturas()
        facturas.Facturas.cargaTablaVentas()
        eventos.Eventos.resizeTablaVentas()
        var.ui.tablaFacturas.clicked.connect(facturas.Facturas.cargaOneFactura)
        var.ui.tablaVentas.clicked.connect(facturas.Facturas.cargaOneVenta)


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
        var.ui.actionListado_Clientes.triggered.connect(informes.Informes.reportClientes)
        var.ui.actionListado_Propiedades.triggered.connect(informes.Informes.abrirInformesProp)


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
        var.ui.btnAltaVen.clicked.connect(lambda: eventos.Eventos.abrirCalendar(2,0))
        var.ui.btnFechaFac.clicked.connect(lambda: eventos.Eventos.abrirCalendar(3, 0))
        var.ui.btnGrabarProp.clicked.connect(propiedades.Propiedades.altaPropiedad)
        var.ui.btnModifProp.clicked.connect(propiedades.Propiedades.modifPropiedad)
        var.ui.btnDelProp.clicked.connect(propiedades.Propiedades.bajaPropiedad)
        var.ui.btnBuscarTipoProp.clicked.connect(propiedades.Propiedades.cargaTablaPropiedades)
        var.ui.btnBuscarCli.clicked.connect(clientes.Clientes.cargaTablaClientes)
        var.ui.BtnSiguienteCli.clicked.connect(clientes.Clientes.siguienteCliente)
        var.ui.BtnAnteriorCli.clicked.connect(clientes.Clientes.anteriorCliente)
        var.ui.BtnSiguienteProp.clicked.connect(propiedades.Propiedades.siguientePropiedad)
        var.ui.BtnAnteriorProp.clicked.connect(propiedades.Propiedades.anteriorPropiedad)
        var.ui.btnGrabarVen.clicked.connect(vendedor.Vendedor.altaVendedor)
        var.ui.BtnDeleteVen.clicked.connect(vendedor.Vendedor.bajaVendedor)
        var.ui.BtnModifVen.clicked.connect(vendedor.Vendedor.modifVendedor)
        var.ui.btnGrabarFactura.clicked.connect(facturas.Facturas.altaFactura)
        var.ui.btnGrabarVenta.clicked.connect(facturas.Facturas.altaVenta)




        '''
        Zona de eventos de las cajas de texto
        '''

        var.ui.txtDniCli.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDniCli.text()))
        var.ui.txtEmailCli.editingFinished.connect(lambda: clientes.Clientes.checkEmail(var.ui.txtEmailCli.text()))
        var.ui.txtMovilCli.editingFinished.connect(lambda: clientes.Clientes.checktelefono(var.ui.txtMovilCli.text()))
        var.ui.txtPrecioVProp.textChanged.connect(lambda: propiedades.Propiedades.manageChkBox(self))
        var.ui.txtPrecioAProp.textChanged.connect(lambda: propiedades.Propiedades.manageChkBox(self))
        var.ui.txtFechaBajaProp.textChanged.connect(lambda: propiedades.Propiedades.manageRadioButtons(self))
        var.ui.txtDniVen.editingFinished.connect(lambda: vendedor.Vendedor.checkDNI(var.ui.txtDniVen.text()))
        var.ui.txtMovilVen.editingFinished.connect(lambda: vendedor.Vendedor.checktelefono(var.ui.txtMovilVen.text()))
        var.ui.txtEmailVen.editingFinished.connect(lambda: vendedor.Vendedor.checkEmail(var.ui.txtEmailVen.text()))
        var.ui.txtFechaFactura.setText(datetime.today().strftime('%d/%m/%Y'))



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
        eventos.Eventos.cargarProvinciasVen(self)

        '''
            Zona de eventos del toolBar
        '''

        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbar_limpiar.triggered.connect(eventos.Eventos.limpiarPanel)
        var.ui.actionExportar_Clientes_CSV.triggered.connect(eventos.Eventos.exportCSVClientes)
        var.ui.actionExportar_Clientes_JSON.triggered.connect(eventos.Eventos.exportJSONClientes)
        var.ui.actionExportar_Propiedades_CSV.triggered.connect(eventos.Eventos.exportCSVProp)
        var.ui.actionExportar_Propiedades_JSON.triggered.connect(eventos.Eventos.exportJSONProp)
        var.ui.actionExportar_Vendedores_JSON.triggered.connect(eventos.Eventos.exportJSONVendedor)


        '''
        Zona de eventos de los checkbox
        '''
        var.ui.chkHistoriaCli.stateChanged.connect(clientes.Clientes.historicoCli)
        var.ui.chkHistoriaProp.stateChanged.connect(propiedades.Propiedades.cargaTablaPropiedades)
        var.ui.chkHistoricoVen.stateChanged.connect(vendedor.Vendedor.cargarTablaVendedores)
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
