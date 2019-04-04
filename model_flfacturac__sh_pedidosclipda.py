# @class_declaration interna_sh_pedidosclipda #
from YBUTILS.viewREST import helpers
from models.flfacturac import models as modelos
import importlib


class interna_sh_pedidosclipda(modelos.mtd_sh_pedidosclipda, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_sh_pedidosclipda #
class sanhigia_informes_sh_pedidosclipda(interna_sh_pedidosclipda, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.accion(aqparam=["oParam"])
    def enviarPedidoPDA(self, oParam):
        return form.iface.enviarPedidoPDA(self, oParam)

    def dameCamposCab(self, idPedido):
        return self.ctx.sanhigia_informes_dameCamposCab(self, idPedido)

    def dameSelectCabXML(self):
        return self.ctx.sanhigia_informes_dameSelectCabXML(self)

    def dameCamposLineas(self, idPedido):
        return self.ctx.sanhigia_informes_dameCamposLineas(self, idPedido)

    def dameSelectLineaXML(self):
        return self.ctx.sanhigia_informes_dameSelectLineaXML(self)

    def queryGrid_histArticulosCli(model, filters):
        return form.iface.queryGrid_histArticulosCli(model, filters)

    def field_colorRow(self):
        return form.iface.field_colorRow(self)

    def datosConfigMailPDA(self):
        return form.iface.datosConfigMailPDA(self)


# @class_declaration sh_pedidosclipda #
class sh_pedidosclipda(sanhigia_informes_sh_pedidosclipda, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfacturac.sh_pedidosclipda_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
