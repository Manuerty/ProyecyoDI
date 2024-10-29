import conexion
import var


class Propiedades():

    def altaTipoPropiedad(self):
        try:
            tipo = var.dlggestion.ui.txtTipoProp.text().title()
            registro = conexion.Conexion.altaTipoProp(tipo)
            var.ui.cmbTipoProp.clear()
            var.ui.cmbTipoProp.addItems(registro)
            var.dlggestion.ui.txtTipoProp.setText('')
        except Exception as error:
            print('Error altaTipoPropiedad: %s ' % str(error))

    # def bajaTipoPropiedad(self):
    #     try:
    #         tipo = var.dlggestion.ui.txtTipoProp.text().title()
    #         conexion.Conexion.bajaTipoProp(tipo)
    #     except Exception as error:
    #         print('Error bajaTipoPropiedad: %s ' % str(error))



