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

    def field_nombreagente(model):
        return form.iface.field_nombreagente(model)

    def checkCodAgente(cursor):
        return form.iface.checkCodAgente(cursor)

    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

    def generarReport(self):
        return form.iface.generarReport(self)

    # def report_ventasarticulo(self, model):
    #     return form.iface.report_ventasarticulo(self, model)

    # @helpers.decoradores.accion()
    # def dameInformeVentasarticulo(self, model):
    #     return form.iface.dameInformeVentasarticulo(self, model)


# @class_declaration i_sh_ventasarticulo #
class i_sh_ventasarticulo(sanhigia_informes_i_sh_ventasarticulo, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactinfo.i_sh_ventasarticulo_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
