# @class_declaration interna_novedades #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_novedades(modelos.mtd_novedades, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_novedades #
class sanhigia_informes_novedades(interna_novedades, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def field_adjunto(self):
        return form.iface.field_adjunto(self)

    def checkButtonDescarga(cursor):
        return form.iface.checkButtonDescarga(cursor)


# @class_declaration novedades #
class novedades(sanhigia_informes_novedades, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface():
        return form.iface


definitions = importlib.import_module("models.flfactalma.novedades_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
