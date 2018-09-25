# @class_declaration interna_sh_pedidosclipda #
from YBUTILS.viewREST import helpers
from models.flfacturac import models as modelos
import importlib


class interna_presupuestoscli(modelos.mtd_presupuestoscli, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_presupuestoscli #
class sanhigia_informes_presupuestoscli(interna_presupuestoscli, helpers.MixinConAcciones):
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

    def imprimirPresupuestoPDA(self):
        return form.iface.imprimirPresupuestoPDA(self)

    def queryGrid_histArticulosCli(model):
        return form.iface.queryGrid_histArticulosCli(model)

    def field_colorRow(self):
        return form.iface.field_colorRow(self)

    def checkCondiciones(cursor):
        return form.iface.checkCondiciones(cursor)

# @class_declaration presupuestoscli #
class presupuestoscli(sanhigia_informes_presupuestoscli, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


definitions = importlib.import_module("models.flfacturac.presupuestoscli_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface