
# @class_declaration sanhigia_informes_pedidoscli #
class sanhigia_informes_pedidoscli(flfacturac_pedidoscli, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def enviarPedidoPDA(self, oParam):
        return form.iface.enviarPedidoPDA(self, oParam)

    def dameCamposCab(self, idPedido):
        return self.ctx.sanhigia_informes_dameCamposCab(self, idPedido)

    def dameSelectCabXML(self):
        return self.ctx.sanhigia_informes_dameSelectCabXML(self)

    def dameCamposLineas(self, idPedido):
        return self.ctx.sanhigia_informes_dameCamposLineas(self, idPedido)

    def dameSelectLineaXML(self):
        return self.ctx.sanhigia_informes_dameSelectLineaXML(self)

    def queryGrid_histArticulosCli(model, filters):
        return form.iface.queryGrid_histArticulosCli(model, filters)

    def field_colorRow(self):
        return form.iface.field_colorRow(self)

    def datosConfigMailPDA(self):
        return form.iface.datosConfigMailPDA(self)

    def validateCursor(self):
        return form.iface.validateCursor(self)

    def drawIf_pedidoscliForm(cursor):
        return form.iface.drawIf_pedidoscliForm(cursor)

