# @class_declaration interna_i_sh_ventaspoblacion #
from YBUTILS.viewREST import helpers
from models.flfactinfo import models as modelos
import importlib


class interna_i_sh_ventaspoblacion(modelos.mtd_i_sh_ventaspoblacion, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_i_sh_ventaspoblacion #
class sanhigia_informes_i_sh_ventaspoblacion(interna_i_sh_ventaspoblacion, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def field_nombreagente(cursor):
        return form.iface.field_nombreagente(cursor)

    def checkCodAgente(cursor):
        return form.iface.checkCodAgente(cursor)

    def report_ventaspoblacion(self):
        return form.iface.report_ventaspoblacion(self)

    @helpers.decoradores.accion()
    def dameInformeVentaspoblacion(self):
        return form.iface.dameInformeVentaspoblacion(self)


# @class_declaration i_sh_ventaspoblacion #
class i_sh_ventaspoblacion(sanhigia_informes_i_sh_ventaspoblacion, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactinfo.i_sh_ventaspoblacion_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
