# @class_declaration interna_productosagtrans #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactppal import models as modelos


class interna_productosagtrans(modelos.mtd_productosagtrans, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_productosagtrans #
class sanhigia_informes_productosagtrans(interna_productosagtrans, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration productosagtrans #
class productosagtrans(sanhigia_informes_productosagtrans, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactppal.productosagtrans_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
