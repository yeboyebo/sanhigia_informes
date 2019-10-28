
# @class_declaration sanhigia_informes_lineaspedidoscli #
class sanhigia_informes_lineaspedidoscli(flfacturac_lineaspedidoscli, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def masUno(self, oParam):
        return form.iface.masUno(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def menosUno(self, oParam):
        return form.iface.menosUno(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def modificarCantidad(self, oParam):
        return form.iface.modificarCantidad(self, oParam)

    def cambiarCantidad(self, idLinea, cantidad):
        return form.iface.cambiarCantidad(self, idLinea, cantidad)

    def validateCursor(self):
        return form.iface.validateCursor(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def cambiarPrecio(self, oParam):
        return form.iface.cambiarPrecio(self, oParam)

    def field_titulo(self):
        return form.iface.field_titulo(self)

    def field_calCantidad(self):
        return form.iface.field_calCantidad(self)

    def field_calTotal(self):
        return form.iface.field_calTotal(self)

    def field_colorRow(self):
        return form.iface.field_colorRow(self)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def borrarLineas(self, oParam):
        return form.iface.borrarLineas(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def copiaLinea(self, oParam):
        return form.iface.copiaLinea(self, oParam)

    def copiaDatosLinea(self, curLP):
        return form.iface.copiaDatosLinea(self, curLP)

    def drawIf_lineaspedidoscliForm(cursor):
        return form.iface.drawIf_lineaspedidoscliForm(cursor)

