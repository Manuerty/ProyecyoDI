from datetime import datetime

from PyQt6.QtCore import QFile
from PyQt6.QtWidgets import QFileDialog

import informes
from dlgAbout import Ui_dlg_About
from dlgCalendar import *
import var
import eventos
import propiedades
from dlgGestionProp import *
from dlgInformeProp import *

class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        var.uicalendar = Ui_dlgCalendar()
        var.uicalendar.setupUi(self)
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year

        var.uicalendar.Calendar.setSelectedDate((QtCore.QDate(ano,mes,dia)))
        var.uicalendar.Calendar.clicked.connect(eventos.Eventos.cargaFecha)


class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()


class dlgGestionProp(QtWidgets.QDialog):
    def __init__(self):
        super(dlgGestionProp, self).__init__()
        self.ui = Ui_dlgGestionProp()
        self.ui.setupUi(self)
        self.ui.btnAltaTipoProp.clicked.connect(propiedades.Propiedades.altaTipoPropiedad)
        self.ui.btnDelTipoProp.clicked.connect(propiedades.Propiedades.bajaTipoPropiedad)

class dlgAbout(QtWidgets.QDialog):
    def __init__(self):
        super(dlgAbout, self).__init__()
        self.ui = Ui_dlg_About()
        self.ui.setupUi(self)
        self.ui.btnCerrarAbout.clicked.connect(eventos.Eventos.cerrarAbout)

class dlgInformeProp(QtWidgets.QDialog):
    def __init__(self):
        super(dlgInformeProp, self).__init__()
        self.ui = Ui_dlgInformeProp()
        self.ui.setupUi(self)
        self.ui.btnGenerarInformeProp.clicked.connect(informes.Informes.reportPropiedades)
