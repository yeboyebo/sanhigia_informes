# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *


class sanhigia_informes(interna):

    def sanhigia_informes_getDesc(self):
        desc = None
        return desc

    def sanhigia_informes_masUno(self, model, oParam):
        _i = self.iface
        idLinea = model.pk
        cantidad = model.cantidad
        cantidad += 1
        return _i.cambiarCantidad(idLinea, cantidad, oParam)

    def sanhigia_informes_menosUno(self, model, oParam):
        _i = self.iface
        idLinea = model.pk
        cantidad = model.cantidad
        if cantidad >= 2:
            cantidad -= 1
        else:
            cantidad = 1
        return _i.cambiarCantidad(idLinea, cantidad, oParam)

    def sanhigia_informes_modificarCantidad(self, model, oParam):
        _i = self.iface
        idLinea = model.pk
        cantidad = oParam['cantidad']
        return _i.cambiarCantidad(idLinea, cantidad, oParam)

    def sanhigia_informes_cambiarCantidad(self, idLinea, cantidad, oParam):
        # print("____________", oParam)
        curLP = qsatype.FLSqlCursor(u"sh_lineaspedidosclipda")
        curLP.select("idlinea = " + str(idLinea))
        if not curLP.first():
            raise ValueError("Error no se encuentra la linea de pedido ")
            return False
        curLP.setModeAccess(curLP.Edit)
        curLP.refreshBuffer()
        curLP.setActivatedBufferCommited(True)
        curLP.setValueBuffer("cantidad", cantidad)
        # curLP.setValueBuffer("referencia", "02314005")
        '''
        curLP.setValueBuffer(u"pvpunitario", qsatype.FactoriaModulos.get('formRecordsh_lineaspedidosclipda').iface.pub_commonCalculateField(u"pvpunitario", curLP))
        curLP.setValueBuffer(u"pvpsindto", qsatype.FactoriaModulos.get('formRecordsh_lineaspedidosclipda').iface.pub_commonCalculateField(u"pvpsindto", curLP))
        curLP.setValueBuffer(u"pvptotal", qsatype.FactoriaModulos.get('formRecordsh_lineaspedidosclipda').iface.pub_commonCalculateField(u"pvptotal", curLP))
        '''

        # Esta comentado para que se instale. Cuando se arregla que salga el mensaje se actualizará. Fecha 14-11-2018
        referencia = curLP.valueBuffer("referencia")
        cantNueva = parseFloat(curLP.valueBuffer("cantidad"))
        codAlmacen = "ALM"
        disponible = qsatype.FLUtil.sqlSelect(u"stocks", u"disponible", ustr(u"referencia = '", referencia, u"' AND codalmacen = '", codAlmacen, u"'"))
        if not disponible:
            disponible = 0
        if cantNueva > parseFloat(disponible):
            if qsatype.FLUtil.sqlSelect(u"articulos", u"referencia", ustr(u"refsustitutivo = '", referencia, u"'")):
                return True
            refSust = qsatype.FLUtil.sqlSelect(u"articulos", u"refsustitutivo", ustr(u"referencia = '", referencia, u"'"))
            # if not refSust or refSust == u"":
            #     return True
            if refSust and refSust != u"":
                if "confirmacion" in oParam and oParam["confirmacion"]:
                    curLP.setValueBuffer("referencia", refSust)
                    qsatype.FactoriaModulos.get('formRecordsh_lineaspedidosclipda').iface.bChCursor("referencia", curLP)
                elif "confirmacion" in oParam and not oParam["confirmacion"]:
                    print("hemos cancelado")
                else:
                    resul = {}
                    resul['status'] = 2
                    resul['confirm'] = "No hay suficiente stock para el artículo " + referencia + " en el almacén " + codAlmacen + ". ¿Desea utilizar su artículo sustitutivo?"
                    resul['oncancel'] = "lanzaraccion"
                    return resul

        qsatype.FactoriaModulos.get('formRecordsh_lineaspedidosclipda').iface.bChCursor("cantidad", curLP)
        if not curLP.commitBuffer():
            return False

        return True

    def sanhigia_informes_validateCursor(self, cursor):
        referencia = cursor.valueBuffer("referencia")
        if referencia is None:
            qsatype.FLUtil.ponMsgError("Error: La referencia no existe o no está selecionada")
            return False
        if qsatype.FLUtil.sqlSelect(u"articulos", u"sevende", ustr(u"referencia = '", referencia, u"'")) is False:
            qsatype.FLUtil.ponMsgError("Error: El artículo {0} ya no se vende. Selecciona otro.".format(referencia))
            return False
        codAlmacen = "ALM"
        # qsatype.FLUtil.sqlSelect(u"pedidoscli", u"codalmacen", ustr(u"idpedido = ", idpedido))
        cantidad = parseFloat(cursor.valueBuffer("cantidad"))
        disponible = qsatype.FLUtil.sqlSelect(u"stocks", u"disponible", ustr(u"referencia = '", referencia, u"' AND codalmacen = '", codAlmacen, u"'"))
        if not disponible:
            disponible = 0
        if cantidad > parseFloat(disponible):
            if qsatype.FLUtil.sqlSelect(u"articulos", u"referencia", ustr(u"refsustitutivo = '", referencia, u"'")):
                return True
            refSust = qsatype.FLUtil.sqlSelect(u"articulos", u"refsustitutivo", ustr(u"referencia = '", referencia, u"'"))
            if not refSust or refSust == u"":
                return True
            else:
                cursor.setValueBuffer("referencia", refSust)
                resul = {}
                resul["resul"] = {}
                resul["resul"]['status'] = 2
                resul["resul"]['confirm'] = "No hay suficiente stock para el artículo " + referencia + " en el almacén " + codAlmacen + ". ¿Desea utilizar su artículo sustitutivo?"
                resul["resul"]['onconfirm'] = "changedata"
                return resul
        return True

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.sanhigia_informes_getDesc()

    def masUno(self, model, oParam):
        return self.ctx.sanhigia_informes_masUno(model, oParam)

    def menosUno(self, model, oParam):
        return self.ctx.sanhigia_informes_menosUno(model, oParam)

    def modificarCantidad(self, model, oParam):
        return self.ctx.sanhigia_informes_modificarCantidad(model, oParam)

    def cambiarCantidad(self, idLinea, cantidad, oParam):
        return self.ctx.sanhigia_informes_cambiarCantidad(idLinea, cantidad, oParam)

    def validateCursor(self, cursor):
        return self.ctx.sanhigia_informes_validateCursor(cursor)


# @class_declaration head #
class head(sanhigia_informes):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super().__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
