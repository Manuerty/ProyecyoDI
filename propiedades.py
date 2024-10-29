import var


class Propiedades():

    def altaTipoPropiedad(self):
        tipo = var.dlggestion.ui.txtTipoProp.text().title()
        print(tipo)