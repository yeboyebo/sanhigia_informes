# @class_declaration interna_dirclientes #
from YBUTILS.viewREST import helpers
from models.flfactppal import models as modelos
import importlib


class interna_dirclientes(modelos.mtd_dirclientes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_dirclientes #
class sanhigia_informes_dirclientes(interna_dirclientes, helpers.MixinConAcciones):
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


# @class_declaration dirclientes #
class dirclientes(sanhigia_informes_dirclientes, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


definitions = importlib.import_module("models.flfactppal.dirclientes_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
