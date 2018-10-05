
# @class_declaration sanhigia_informes_dirclientes #
class sanhigia_informes_dirclientes(alta_clientes_dirclientes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def initValidation(name, data=None):
        return form.iface.initValidation(name, data)

    def iniciaValoresLabel(self, template=None, cursor=None, data=None):
        return form.iface.iniciaValoresLabel(self, template, cursor)

    def bChLabel(fN=None, cursor=None):
        return form.iface.bChLabel(fN, cursor)

    def getFilters(self, name, template=None):
        return form.iface.getFilters(self, name, template)

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def getDesc():
        return form.iface.getDesc()

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getDireccion(self, oParam):
        return form.iface.getDireccion(self, oParam)

    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

