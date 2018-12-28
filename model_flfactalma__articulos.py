
# @class_declaration sanhigia_informes_articulos #
class sanhigia_informes_articulos(flfactalma_articulos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def subirLinea(self, oParam, cursor):
        return form.iface.subirLinea(self, oParam, cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def insertarLinea(self, oParam):
        return form.iface.insertarLinea(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam", "cursor"])
    def subirLineapres(self, oParam, cursor):
        return form.iface.subirLineaPres(self, oParam, cursor)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def insertarLineaPres(self, oParam):
        return form.iface.insertarLineaPres(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getReferenciaDesc(self, oParam):
        return form.iface.getReferenciaDesc(self, oParam)

