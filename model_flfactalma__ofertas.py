# @class_declaration interna_ofertas #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_ofertas(modelos.mtd_ofertas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_ofertas #
class sanhigia_informes_ofertas(interna_ofertas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration ofertas #
class ofertas(sanhigia_informes_ofertas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface():
        return form.iface


definitions = importlib.import_module("models.flfactalma.ofertas_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
