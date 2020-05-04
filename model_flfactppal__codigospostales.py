# @class_declaration interna_codigospostales #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactppal import models as modelos


class interna_codigospostales(modelos.mtd_codigospostales, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_codigospostales #
class sanhigia_informes_codigospostales(interna_codigospostales, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration codigospostales #
class codigospostales(sanhigia_informes_codigospostales, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactppal.codigospostales_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
