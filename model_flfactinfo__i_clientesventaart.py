# @class_declaration interna_i_clientesventaart #
from YBUTILS.viewREST import helpers
from models.flfactinfo import models as modelos
import importlib


class interna_i_clientesventaart(modelos.mtd_i_clientesventaart, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_i_clientesventaart #
class sanhigia_informes_i_clientesventaart(interna_i_clientesventaart, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def field_nombreagente(cursor):
        return form.iface.field_nombreagente(cursor)

    def checkCodAgente(cursor):
        return form.iface.checkCodAgente(cursor)

    def report_clientesporarticulo(self):
        return form.iface.report_clientesporarticulo(self)

    @helpers.decoradores.accion()
    def dameInformeClientesporarticulo(self):
        return form.iface.dameInformeClientesporarticulo(self)


# @class_declaration i_clientesventaart #
class i_clientesventaart(sanhigia_informes_i_clientesventaart, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactinfo.i_clientesventaart_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
