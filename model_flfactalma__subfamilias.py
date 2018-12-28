# @class_declaration interna_subfamilias #
from YBUTILS.viewREST import helpers
from models.flfactalma import models as modelos
import importlib


class interna_subfamilias(modelos.mtd_subfamilias, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_subfamilias #
class sanhigia_informes_subfamilias(interna_subfamilias, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration subfamilias #
class subfamilias(sanhigia_informes_subfamilias, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactalma.subfamilias_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
