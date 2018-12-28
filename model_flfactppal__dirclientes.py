
# @class_declaration sanhigia_informes_dirclientes #
class sanhigia_informes_dirclientes(alta_clientes_dirclientes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def getDireccion(self, oParam):
        return form.iface.getDireccion(self, oParam)

