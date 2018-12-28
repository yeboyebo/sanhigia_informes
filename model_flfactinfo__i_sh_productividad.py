# @class_declaration interna_i_sh_productividad #
from YBUTILS.viewREST import helpers
from models.flfactinfo import models as modelos
import importlib


class interna_i_sh_productividad(modelos.mtd_i_sh_productividad, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_i_sh_productividad #
class sanhigia_informes_i_sh_productividad(interna_i_sh_productividad, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def field_nombreagente(cursor):
        return form.iface.field_nombreagente(cursor)

    def checkCodAgente(cursor):
        return form.iface.checkCodAgente(cursor)

# @class_declaration i_sh_productividad #
class i_sh_productividad(sanhigia_informes_i_sh_productividad, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactinfo.i_sh_productividad_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
