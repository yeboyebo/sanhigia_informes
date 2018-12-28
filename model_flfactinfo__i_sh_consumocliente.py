# @class_declaration interna_i_sh_consumocliente #
from YBUTILS.viewREST import helpers
from models.flfactinfo import models as modelos
import importlib


class interna_i_sh_consumocliente(modelos.mtd_i_sh_consumocliente, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_i_sh_consumocliente #
class sanhigia_informes_i_sh_consumocliente(interna_i_sh_consumocliente, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def field_nombreagente(cursor):
        return form.iface.field_nombreagente(cursor)

    def checkCodAgente(cursor):
        return form.iface.checkCodAgente(cursor)

    def report_consumocliente(self):
        return form.iface.report_consumocliente(self)

    @helpers.decoradores.accion()
    def dameInformeConsumocliente(self):
        return form.iface.dameInformeConsumocliente(self)


# @class_declaration i_sh_consumocliente #
class i_sh_consumocliente(sanhigia_informes_i_sh_consumocliente, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactinfo.i_sh_consumocliente_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
