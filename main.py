

import eventos
from ventPrincipal import *
import sys
import var

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_ventPrincipal()
        var.ui.setupUi(self)

        '''
        Zona de eventos del menuBar
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    window.showMaximized()
    sys.exit(app.exec())
