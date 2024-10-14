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
        var.dlgabrir = FileDialogAbrir()
        self.setStyleSheet(style.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        #conexionserver.ConexionServer.crear_conexion(self)

        '''
        Zona de eventos de la tabla
        '''
        clientes.Clientes.cargaTablaClientes(self)
        eventos.Eventos.resizeTablaClientes(self)

        '''
        Zona de eventos del menuBar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_BackUp.triggered.connect(eventos.Eventos.crearBackUp)
        var.ui.actionRestaurar_BackUp.triggered.connect(eventos.Eventos.restaurarBackUp)

        '''
        Zona de eventos de los botones
        '''

        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))

        '''
        Zona de eventos de las cajas de texto
        '''

        var.ui.txtDniCli.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDniCli.text()))
        var.ui.txtEmailCli.editingFinished.connect(lambda: clientes.Clientes.checkEmail(var.ui.txtEmailCli.text()))
        '''
        combobox events
        
        '''
        eventos.Eventos.cargarProvincias(self)
        eventos.Eventos.cargarMunicipios(self)
        var.ui.cmbProCli.currentIndexChanged.connect(eventos.Eventos.cargarMunicipios)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    window.showMaximized()
    sys.exit(app.exec())
