
# @class_declaration sanhigia_informes #
class sanhigia_informes(flfacturac):

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
        super().__init__(context)

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

