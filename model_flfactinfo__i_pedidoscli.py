# @class_declaration sanhigia_informes_i_pedidoscli #
class sanhigia_informes_i_pedidoscli(flfactinfo_i_pedidoscli, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def field_nombreagente(cursor):
        return form.iface.field_nombreagente(cursor)

    def checkCodAgente(cursor):
        return form.iface.checkCodAgente(cursor)

    def report_pedidoscli(self, cursor):
        return form.iface.report_pedidoscli(self, cursor)

    @helpers.decoradores.accion()
    def dameInformePedidoscli(self):
        return form.iface.dameInformePedidoscli(self)
