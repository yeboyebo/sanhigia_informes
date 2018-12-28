# @class_declaration interna_gd_config #
import importlib

from YBUTILS.viewREST import helpers

from models.flcolagedo import models as modelos


class interna_gd_config(modelos.mtd_gd_config, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_gd_config #
class sanhigia_informes_gd_config(interna_gd_config, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration gd_config #
class gd_config(sanhigia_informes_gd_config, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flcolagedo.gd_config_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
