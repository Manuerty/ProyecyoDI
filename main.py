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

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_ventPrincipal()
        var.ui.setupUi(self)
        var.uicalendar= Calendar()
        var.dlggestion = dlgGestionprop()
        var.dlgabrir = FileDialogAbrir()
        var.historico = 1
        self.setStyleSheet(style.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        #conexionserver.ConexionServer.crear_conexion(self)
        clientes.Clientes.cargaTablaClientes(self)



        '''
        Zona de eventos de la tabla
        '''
        eventos.Eventos.resizeTablaClientes(self)
        var.ui.tablaClientes.clicked.connect(clientes.Clientes.cargaOneCliente)
        eventos.Eventos.resizeTablaPropiedades(self)

        '''
        Zona de eventos del menuBar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_BackUp.triggered.connect(eventos.Eventos.crearBackUp)
        var.ui.actionRestaurar_BackUp.triggered.connect(eventos.Eventos.restaurarBackUp)
        var.ui.actionTipoPropiedad.triggered.connect(eventos.Eventos.abrirTipoProp)


        '''
        Zona de eventos de los botones
        '''

        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0, 0))
        var.ui.btnBajaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0, 1))
        var.ui.btnModifiCli.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnDelCli.clicked.connect(clientes.Clientes.bajaCliente)

        '''
        Zona de eventos de las cajas de texto
        '''

        var.ui.txtDniCli.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDniCli.text()))
        var.ui.txtEmailCli.editingFinished.connect(lambda: clientes.Clientes.checkEmail(var.ui.txtEmailCli.text()))
        var.ui.txtMovilCli.editingFinished.connect(lambda: clientes.Clientes.checktelefono(var.ui.txtMovilCli.text()))
        '''
        combobox events
        
        '''
        eventos.Eventos.cargarProvincias(self)
        eventos.Eventos.cargarMunicipios(self)
        var.ui.cmbProCli.currentIndexChanged.connect(eventos.Eventos.cargarMunicipios)

        '''
            Zona de eventos del toolBar
        '''

        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbar_limpiar.triggered.connect(eventos.Eventos.limpiarPanel)


        '''
        Zona de eventos de los checkbox
        '''
        var.ui.chkHistoriaCli.stateChanged.connect(clientes.Clientes.historicoCli)



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())
