# @class_declaration interna_i_sh_ventasfamilia #
from YBUTILS.viewREST import helpers
from models.flfactinfo import models as modelos
import importlib


class interna_i_sh_ventasfamilia(modelos.mtd_i_sh_ventasfamilia, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_i_sh_ventasfamilia #
class sanhigia_informes_i_sh_ventasfamilia(interna_i_sh_ventasfamilia, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def field_nombreagente(model):
        return form.iface.field_nombreagente(model)

    def iniciaValoresCursor(cursor=None):
        return form.iface.iniciaValoresCursor(cursor)

    def checkCodAgente(cursor):
        return form.iface.checkCodAgente(cursor)

    def generarReport(self):
        return form.iface.generarReport(self)


# @class_declaration i_sh_ventasfamilia #
class i_sh_ventasfamilia(sanhigia_informes_i_sh_ventasfamilia, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactinfo.i_sh_ventasfamilia_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
