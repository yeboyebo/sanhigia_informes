
# @class_declaration sanhigia_informes_dirclientes #
class sanhigia_informes_dirclientes(alta_clientes_dirclientes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getDireccion(self, oParam):
        return form.iface.getDireccion(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def generaMapaDirecciones(self, model, template):
        return form.iface.generaMapaDirecciones(model, template)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getMapaDirecciones(self, oParam):
        return form.iface.getMapaDirecciones(oParam)

    # def validateCursor(self):
    #     return form.iface.validateCursor(self)

