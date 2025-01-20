import conexion
import var


class facturas:
    def altaFactura(self):
        try:
            nuevaFactura = [var.ui.lblfac.text(), var.ui.txtFechaFac.text(), var.ui.txtCliFac.text()]

        except Exception as error:
            print('Error alta factura: %s' % str(error))