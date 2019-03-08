# @class_declaration interna_sh_previsiones #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactppal import models as modelos


class interna_sh_previsiones(modelos.mtd_sh_previsiones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_sh_previsiones #
class sanhigia_informes_sh_previsiones(interna_sh_previsiones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sh_previsiones #
class sh_previsiones(sanhigia_informes_sh_previsiones, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactppal.sh_previsiones_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
