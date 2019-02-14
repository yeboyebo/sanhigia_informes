
# @class_declaration sanhigia_informes_presupuestoscli #
class sanhigia_informes_presupuestoscli(flfacturac_presupuestoscli, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def imprimirPresupuestoPDA(self):
        return form.iface.imprimirPresupuestoPDA(self)

    def queryGrid_histArticulosCli(model, filters):
        return form.iface.queryGrid_histArticulosCli(model, filters)

    def field_colorRow(self):
        return form.iface.field_colorRow(self)

    def checkCondiciones(cursor):
        return form.iface.checkCondiciones(cursor)

