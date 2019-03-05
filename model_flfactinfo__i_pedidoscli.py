
# @class_declaration sanhigia_informes_i_pedidoscli #
class sanhigia_informes_i_pedidoscli(flfactinfo_i_pedidoscli, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def bChCursor(fN, cursor):
        return form.iface.bChCursor(fN, cursor)

    def field_nombreagente(model):
        return form.iface.field_nombreagente(model)

    def field_nombrecliente(model):
        return form.iface.field_nombrecliente(model)

    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

    def checkCodAgente(cursor):
        return form.iface.checkCodAgente(cursor)

    def generarReport(self):
        return form.iface.generarReport(self)

    # def report_pedidoscli(self, cursor):
    #     return form.iface.report_pedidoscli(self, cursor)

    # @helpers.decoradores.accion()
    # def dameInformePedidoscli(self):
    #     return form.iface.dameInformePedidoscli(self)

