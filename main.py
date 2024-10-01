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
        self.setStyleSheet(style.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        eventos.Eventos.cargarProvincias(self)
        eventos.Eventos.cargarMunicipios(self)

        '''
        Zona de eventos del menuBar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)

        '''
        Zona de eventos de los botones
        '''

        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaCliente)

        '''
        Zona de eventos de las cajas de texto
        '''

        var.ui.txtDniCli.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDniCli.text()))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    window.showMaximized()
    sys.exit(app.exec())
