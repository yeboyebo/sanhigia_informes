# @class_declaration interna_i_sh_ventasarticulo #
from YBUTILS.viewREST import helpers
from models.flfactinfo import models as modelos
import importlib


class interna_i_sh_ventasarticulo(modelos.mtd_i_sh_ventasarticulo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_i_sh_ventasarticulo #
class sanhigia_informes_i_sh_ventasarticulo(interna_i_sh_ventasarticulo, helpers.MixinConAcciones):
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

    def field_nombreagente(cursor):
        return form.iface.field_nombreagente(cursor)

    def checkCodAgente(cursor):
        return form.iface.checkCodAgente(cursor)

    def report_ventasarticulo(self):
        return form.iface.report_ventasarticulo(self)

    @helpers.decoradores.accion()
    def dameInformeVentasarticulo(self):
        return form.iface.dameInformeVentasarticulo(self)


# @class_declaration i_sh_ventasarticulo #
class i_sh_ventasarticulo(sanhigia_informes_i_sh_ventasarticulo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


definitions = importlib.import_module("models.flfactinfo.i_sh_ventasarticulo_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
