# @class_declaration interna_sh_lineaspedidosclipda #
from YBUTILS.viewREST import helpers
from models.flfacturac import models as modelos
import importlib


class interna_sh_lineaspedidosclipda(modelos.mtd_sh_lineaspedidosclipda, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration sanhigia_informes_sh_lineaspedidosclipda #
class sanhigia_informes_sh_lineaspedidosclipda(interna_sh_lineaspedidosclipda, helpers.MixinConAcciones):
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
    def masUno(self, oParam):
        return form.iface.masUno(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def menosUno(self, oParam):
        return form.iface.menosUno(self, oParam)

    @helpers.decoradores.accion(aqparam=["oParam"])
    def modificarCantidad(self, oParam):
        return form.iface.modificarCantidad(self, oParam)

    def cambiarCantidad(self, idLinea, cantidad):
        return form.iface.cambiarCantidad(self, idLinea, cantidad)

    def validateCursor(self):
        return form.iface.validateCursor(self)


# @class_declaration sh_lineaspedidosclipda #
class sh_lineaspedidosclipda(sanhigia_informes_sh_lineaspedidosclipda, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


definitions = importlib.import_module("models.flfacturac.sh_lineaspedidosclipda_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
