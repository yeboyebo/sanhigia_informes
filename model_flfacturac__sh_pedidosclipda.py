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

    def initValidation(name, data=None):
        return form.iface.initValidation(name, data)

    def iniciaValoresLabel(self, template=None, cursor=None, data=None):
        return form.iface.iniciaValoresLabel(self, template, cursor)

    def bChLabel(fN=None, cursor=None):
        return form.iface.bChLabel(fN, cursor)

    def getFilters(self, name, template=None):
        return form.iface.getFilters(self, name, template)

    def getForeignFields(self, template=None):
        return form.iface.getForeignFields(self, template)

    def getDesc():
        return form.iface.getDesc()

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

    def queryGrid_histArticulosCli(model):
        return form.iface.queryGrid_histArticulosCli(model)

    def field_colorRow(self):
        return form.iface.field_colorRow(self)

    def datosConfigMailPDA(self):
        return form.iface.datosConfigMailPDA(self)


# @class_declaration sh_pedidosclipda #
class sh_pedidosclipda(sanhigia_informes_sh_pedidosclipda, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


definitions = importlib.import_module("models.flfacturac.sh_pedidosclipda_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
