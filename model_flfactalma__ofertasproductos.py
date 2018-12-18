# @class_declaration interna_ofertasproductos #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_ofertasproductos(modelos.mtd_ofertasproductos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_ofertasproductos #
class sanhigia_informes_ofertasproductos(interna_ofertasproductos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def field_adjunto(self):
        return form.iface.field_adjunto(self)


# @class_declaration ofertasproductos #
class ofertasproductos(sanhigia_informes_ofertasproductos, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface():
        return form.iface


definitions = importlib.import_module("models.flfactalma.ofertasproductos_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
