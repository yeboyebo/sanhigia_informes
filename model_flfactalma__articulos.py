# @class_declaration interna_articulos #
from YBUTILS.viewREST import helpers
from models.flfactalma import models as modelos
import importlib


class interna_articulos(modelos.mtd_articulos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_articulos #
class sanhigia_informes_articulos(interna_articulos, helpers.MixinConAcciones):
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


# @class_declaration articulos #
class articulos(sanhigia_informes_articulos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


definitions = importlib.import_module("models.flfactalma.articulos_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
