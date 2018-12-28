# @class_declaration interna_i_pedidoscli #
from YBUTILS.viewREST import helpers
from models.flfactinfo import models as modelos
import importlib


class interna_i_pedidoscli(modelos.mtd_i_pedidoscli, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_i_pedidoscli #
class sanhigia_informes_i_pedidoscli(interna_i_pedidoscli, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def field_nombreagente(cursor):
        return form.iface.field_nombreagente(cursor)

    def checkCodAgente(cursor):
        return form.iface.checkCodAgente(cursor)

    def report_pedidoscli(self, cursor):
        return form.iface.report_pedidoscli(self, cursor)

    @helpers.decoradores.accion()
    def dameInformePedidoscli(self):
        return form.iface.dameInformePedidoscli(self)


# @class_declaration i_pedidoscli #
class i_pedidoscli(sanhigia_informes_i_pedidoscli, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactinfo.i_pedidoscli_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
