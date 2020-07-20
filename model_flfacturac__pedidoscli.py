
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

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def eliminarPedido(self, oParam, cursor):
        return form.iface.eliminarPedido(self, oParam, cursor)

    def drawIf_verSeguimiento(cursor):
        return form.iface.drawIf_verSeguimiento(cursor)

    @helpers.decoradores.accion(aqparam=[])
    def visualizarSeguimiento(self):
        return form.iface.visualizarSeguimiento(self)

    def dameObjetoSeguimientos(self, idpedido):
        return self.ctx.sanhigia_informes_dameObjetoSeguimientos(self, idpedido)

    def dameCuerpoEmailPrueba(self):
        return self.ctx.sanhigia_informes_dameCuerpoEmailPrueba(self)

    def drawIf_deshabilitarCampos(cursor):
        return form.iface.drawIf_deshabilitarCampos(cursor)

