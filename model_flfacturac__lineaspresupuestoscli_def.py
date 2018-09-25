# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *


class sanhigia_informes(interna):

    def sanhigia_informes_initValidation(self, name, data=None):
        response = True
        return response

    def sanhigia_informes_iniciaValoresLabel(self, model=None, template=None, cursor=None):
        labels = {}
        return labels

    def sanhigia_informes_bChLabel(self, fN=None, cursor=None):
        labels = {}
        return labels

    def sanhigia_informes_getFilters(self, model, name, template=None):
        filters = []
        return filters

    def sanhigia_informes_getForeignFields(self, model, template=None):
        fields = []
        return fields

    def sanhigia_informes_getDesc(self):
        desc = None
        return desc

    def sanhigia_informes_masUno(self, model):
        _i = self.iface
        idLinea = model.pk
        deCondiciones = qsatype.FLUtil.sqlSelect(u"presupuestoscli p INNER JOIN lineaspresupuestoscli lp ON p.idpresupuesto = lp.idpresupuesto", u"p.decondiciones", ustr(u"lp.idlinea = ", idLinea))
        if deCondiciones is not True:
            cantidad = model.cantidad
            cantidad += 1
            if not _i.cambiarCantidad(idLinea, cantidad):
                return False
        else:
            resul = {}
            resul['status'] = -3
            resul['msg'] = "El presupuesto es de condiciones. No se puede modificar la cantidad"
            return resul
            # return True
        return True

    def sanhigia_informes_menosUno(self, model):
        _i = self.iface
        idLinea = model.pk
        deCondiciones = qsatype.FLUtil.sqlSelect(u"presupuestoscli p INNER JOIN lineaspresupuestoscli lp ON p.idpresupuesto = lp.idpresupuesto", u"p.decondiciones", ustr(u"lp.idlinea = ", idLinea))
        if deCondiciones is not True:
            cantidad = model.cantidad
            if cantidad >= 2:
                cantidad -= 1
            else:
                cantidad = 1
            if not _i.cambiarCantidad(idLinea, cantidad):
                return False
        else:
            resul = {}
            resul['status'] = -3
            resul['msg'] = "El presupuesto es de condiciones. No se puede modificar la cantidad"
            return resul
            # return True
        return True

    def sanhigia_informes_modificarCantidad(self, model, oParam):
        _i = self.iface
        idLinea = model.pk
        deCondiciones = qsatype.FLUtil.sqlSelect(u"presupuestoscli p INNER JOIN lineaspresupuestoscli lp ON p.idpresupuesto = lp.idpresupuesto", u"p.decondiciones", ustr(u"lp.idlinea = ", idLinea))
        if deCondiciones is not True:
            cantidad = oParam['cantidad']
            if not _i.cambiarCantidad(idLinea, cantidad):
                return False
        else:
            resul = {}
            resul['status'] = -3
            resul['msg'] = "El presupuesto es de condiciones. No se puede modificar la cantidad"
            return resul
            # return True
        return True

    def sanhigia_informes_cambiarCantidad(self, idLinea, cantidad):
        curLP = qsatype.FLSqlCursor(u"lineaspresupuestoscli")
        curLP.select("idlinea = " + str(idLinea))
        if not curLP.first():
            raise ValueError("Error no se encuentra la linea de presupuesto")
            return False
        curLP.setModeAccess(curLP.Edit)
        curLP.refreshBuffer()
        curLP.setActivatedBufferCommited(True)
        curLP.setValueBuffer("cantidad", str(cantidad))
        qsatype.FactoriaModulos.get('formRecordlineaspresupuestoscli').iface.bChCursor("cantidad", curLP)
        if not curLP.commitBuffer():
            return False
        return True

    def sanhigia_informes_checkCondicionesLinea(self, cursor):
        idPresupuesto = cursor.valueBuffer("idpresupuesto")
        deCondiciones = qsatype.FLUtil.sqlSelect(u"presupuestoscli", u"decondiciones", ustr(u"idpresupuesto = ", idPresupuesto))
        if deCondiciones is True:
            return "disabled"
        return True

    def sanhigia_informes_validateCursor(self, cursor):
        referencia = cursor.valueBuffer("referencia")
        if referencia is None:
            qsatype.FLUtil.ponMsgError("Error: La referencia no existe o no está selecionada")
            return False
        return True

    def __init__(self, context=None):
        super(sanhigia_informes, self).__init__(context)

    def initValidation(self, name, data=None):
        return self.ctx.sanhigia_informes_initValidation(name, data=None)

    def iniciaValoresLabel(self, model=None, template=None, cursor=None):
        return self.ctx.sanhigia_informes_iniciaValoresLabel(model, template, cursor)

    def bChLabel(self, fN=None, cursor=None):
        return self.ctx.sanhigia_informes_bChLabel(fN, cursor)

    def getFilters(self, model, name, template=None):
        return self.ctx.sanhigia_informes_getFilters(model, name, template)

    def getForeignFields(self, model, template=None):
        return self.ctx.sanhigia_informes_getForeignFields(model, template)

    def getDesc(self):
        return self.ctx.sanhigia_informes_getDesc()

    def masUno(self, model):
        return self.ctx.sanhigia_informes_masUno(model)

    def menosUno(self, model):
        return self.ctx.sanhigia_informes_menosUno(model)

    def modificarCantidad(self, model, oParam):
        return self.ctx.sanhigia_informes_modificarCantidad(model, oParam)

    def cambiarCantidad(self, idLinea, cantidad):
        return self.ctx.sanhigia_informes_cambiarCantidad(idLinea, cantidad)

    def checkCondicionesLinea(self, cursor):
        return self.ctx.sanhigia_informes_checkCondicionesLinea(cursor)

    def validateCursor(self, cursor):
        return self.ctx.sanhigia_informes_validateCursor(cursor)


# @class_declaration head #
class head(sanhigia_informes):

    def __init__(self, context=None):
        super(head, self).__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super(ifaceCtx, self).__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
