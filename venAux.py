from datetime import datetime

from PyQt6 import QtSql
from PyQt6.QtCore import QFile
from PyQt6.QtWidgets import QFileDialog, QCompleter

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

        # Inicializa el combo box con un elemento vacío
        self.ui.cmbMuniInforme.addItem("")

        # Obtén la lista de municipios
        municipios = dlgInformeProp.listaProvForInforme()

        # Agrega cada municipio individualmente al combo box
        for municipio in municipios:
            self.ui.cmbMuniInforme.addItem(municipio)

        # Configura el autocompletado con la lista de municipios
        completar = QCompleter(municipios, self)
        completar.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completar.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self.ui.cmbMuniInforme.setCompleter(completar)

        # Configura el botón de generar informe
        self.ui.btnGenerarInformeProp.clicked.connect(self.generateReport)

    @staticmethod
    def listaProvForInforme():
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT municipio FROM municipios")
        if query.exec():
            while query.next():
                listaprov.append(query.value(0))
        else:
            print(query.lastError().text())
        return listaprov


    def generateReport(self):
        municipio = self.ui.cmbMuniInforme.currentText()
        informes.Informes.reportPropiedades(municipio)
        self.close()

