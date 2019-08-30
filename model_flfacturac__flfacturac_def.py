
# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *
from YBUTILS.viewREST import cacheController


class sanhigia_informes(flfacturac):

    def sanhigia_informes_bufferCommited_lineaspresupuestoscli(self, curLinea=None):
        # _i = self.iface
        curPresupuesto = qsatype.FLSqlCursor(u"presupuestoscli")
        curPresupuesto.select(ustr(u"idpresupuesto = ", curLinea.valueBuffer(u"idpresupuesto")))
        if not curPresupuesto.first():
            return False
        curPresupuesto.setModeAccess(curPresupuesto.Edit)
        curPresupuesto.refreshBuffer()
        if not qsatype.FactoriaModulos.get('formRecordpresupuestoscli').iface.calcularTotalesCursor(curPresupuesto):
            return False
        if not curPresupuesto.commitBuffer():
            return False
        return True

    def sanhigia_informes_bufferCommited_lineaspedidoscli(self, curLinea=None):
        # _i = self.iface
        curPedido = qsatype.FLSqlCursor(u"pedidoscli")
        curPedido.select(ustr(u"idpedido = ", curLinea.valueBuffer(u"idpedido")))
        if not curPedido.first():
            return False
        curPedido.setModeAccess(curPedido.Edit)
        curPedido.refreshBuffer()
        if not qsatype.FactoriaModulos.get('formRecordpedidoscli').iface.calcularTotalesCursor(curPedido):
            return False
        if not curPedido.commitBuffer():
            return False
        return True

    def sanhigia_informes_bufferCommited_lineasfacturascli(self, curLinea=None):
        # _i = self.iface
        curFactura = qsatype.FLSqlCursor(u"facturascli")
        curFactura.select(ustr(u"idfactura = ", curLinea.valueBuffer(u"idfactura")))
        if not curFactura.first():
            return False
        curFactura.setModeAccess(curFactura.Edit)
        curFactura.refreshBuffer()
        if not qsatype.FactoriaModulos.get('formRecordfacturascli').iface.calcularTotalesCursor(curFactura):
            return False
        if not curFactura.commitBuffer():
            return False
        return True

    def sanhigia_informes_bufferCommited_lineasalbaranescli(self, curLinea=None):
        # _i = self.iface
        curAlbaran = qsatype.FLSqlCursor(u"albaranescli")
        curAlbaran.select(ustr(u"idalbaran = ", curLinea.valueBuffer(u"idalbaran")))
        if not curAlbaran.first():
            return False
        curAlbaran.setModeAccess(curAlbaran.Edit)
        curAlbaran.refreshBuffer()
        if not qsatype.FactoriaModulos.get('formRecordalbaranescli').iface.calcularTotalesCursor(curAlbaran):
            return False
        if not curAlbaran.commitBuffer():
            return False
        return True

    def sanhigia_informes_bufferCommited_sh_lineaspedidosclipda(self, curLinea=None):
        # _i = self.iface
        curPedido = qsatype.FLSqlCursor(u"sh_pedidosclipda")
        curPedido.select(ustr(u"idpedido = ", curLinea.valueBuffer(u"idpedido")))
        if not curPedido.first():
            return False
        curPedido.setModeAccess(curPedido.Edit)
        curPedido.refreshBuffer()
        if not qsatype.FactoriaModulos.get('formRecordsh_pedidosclipda').iface.calcularTotalesCursor(curPedido):
            return False
        if not curPedido.commitBuffer():
            return False
        return True

    def sanhigia_informes_bufferCommited_presupuestoscli(self, curPresupuesto=None):
        return True

    def __init__(self, context=None):
        super().__init__(context)

    def bufferCommited_lineaspresupuestoscli(self, curLinea=None):
        return self.ctx.sanhigia_informes_bufferCommited_lineaspresupuestoscli(curLinea)

    def bufferCommited_lineaspedidoscli(self, curLinea=None):
        return self.ctx.sanhigia_informes_bufferCommited_lineaspedidoscli(curLinea)

    def bufferCommited_lineasfacturascli(self, curLinea=None):
        return self.ctx.sanhigia_informes_bufferCommited_lineasfacturascli(curLinea)

    def bufferCommited_lineasalbaranescli(self, curLinea=None):
        return self.ctx.sanhigia_informes_bufferCommited_lineasalbaranescli(curLinea)

    def bufferCommited_sh_lineaspedidosclipda(self, curLinea=None):
        return self.ctx.sanhigia_informes_bufferCommited_sh_lineaspedidosclipda(curLinea)

    def bufferCommited_presupuestoscli(self, curPresupuesto=None):
        return self.ctx.sanhigia_informes_bufferCommited_presupuestoscli(curPresupuesto)

