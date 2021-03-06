
# @class_declaration sanhigia_informes_clientes #
class sanhigia_informes_clientes(alta_clientes_clientes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getCliente(self, oParam):
        return form.iface.getCliente(self, oParam)

    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_clientesInactivos(model, filters):
        return form.iface.queryGrid_clientesInactivos(model, filters)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_clientesInactivos_initFilter(model=None):
        return form.iface.queryGrid_clientesInactivos_initFilter()

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_ventasClientes(model, filters):
        return form.iface.queryGrid_ventasClientes(model, filters)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_clientesNuevos(model, filters):
        return form.iface.queryGrid_clientesNuevos(model, filters)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def queryGrid_comparativas(model, filters):
        return form.iface.queryGrid_comparativas(model, filters)

    def validateCursor(self):
        return form.iface.validateCursor(self)

    def drawIf_deshabilitarCamposGBComercial(cursor):
        return form.iface.drawIf_deshabilitarCamposGBComercial(cursor)

