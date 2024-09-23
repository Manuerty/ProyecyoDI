from ventPrincipal import *
import sys

class Main(QtWidgets.QMainWindow):
git
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_ventPrincipal()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())