
# @class_declaration sanhigia_informes_lineaspresupuestoscli #
class sanhigia_informes_lineaspresupuestoscli(flfacturac_lineaspresupuestoscli, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion()
    def masUno(self):
        return form.iface.masUno(self)

    @helpers.decoradores.accion()
    def menosUno(self):
        return form.iface.menosUno(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def modificarCantidad(self, oParam):
        return form.iface.modificarCantidad(self, oParam)

    def cambiarCantidad(self, idLinea, cantidad):
        return form.iface.cambiarCantidad(self, idLinea, cantidad)

    def checkCondicionesLinea(cursor):
        return form.iface.checkCondicionesLinea(cursor)

    def validateCursor(self):
        return form.iface.validateCursor(self)

