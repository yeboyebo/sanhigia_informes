
# @class_declaration sanhigia_informes #
class sanhigia_informes(flfacturac):

    def sanhigia_informes_masUno(self, model):
        _i = self.iface
        idLinea = model.pk
        deCondiciones = qsatype.FLUtil.sqlSelect(u"presupuestoscli p INNER JOIN lineaspresupuestoscli lp ON p.idpresupuesto = lp.idpresupuesto", u"p.decondiciones", ustr(u"lp.idlinea = ", idLinea))
        if deCondiciones is not True:
            cantidad = model.cantidad
            cantidad += 1
            cantMultiplos = qsatype.FLUtil.sqlSelect(u"articulos", u"sh_canmultiplovta", u"referencia = '{}'".format(model.referencia.referencia))
            if not cantMultiplos or cantMultiplos == u"" or cantMultiplos == 0:
                if not _i.cambiarCantidad(idLinea, cantidad):
                    return False
            elif cantidad % cantMultiplos != 0:
                resul = {}
                resul['status'] = -3
                resul['msg'] = "La referencia {0} tiene activada la opción múltiplos de cantidad.<br>La cantidad debe ser múltipla a {1}".format(model.referencia.referencia, cantMultiplos)
                return resul
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
            cantMultiplos = qsatype.FLUtil.sqlSelect(u"articulos", u"sh_canmultiplovta", u"referencia = '{}'".format(model.referencia.referencia))
            if not cantMultiplos or cantMultiplos == u"" or cantMultiplos == 0:
                if not _i.cambiarCantidad(idLinea, cantidad):
                    return False
            elif cantidad % cantMultiplos != 0:
                resul = {}
                resul['status'] = -3
                resul['msg'] = "La referencia {0} tiene activada la opción múltiplos de cantidad.<br>La cantidad debe ser múltipla a {1}".format(model.referencia.referencia, cantMultiplos)
                return resul
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
            cantMultiplos = qsatype.FLUtil.sqlSelect(u"articulos", u"sh_canmultiplovta", u"referencia = '{}'".format(model.referencia.referencia))
            if cantMultiplos and cantMultiplos is not None and cantMultiplos != 0 and int(cantidad) % cantMultiplos != 0:
                resul = {}
                resul['status'] = -3
                resul['msg'] = "La referencia {0} tiene activada la opción múltiplos de cantidad.<br>La cantidad debe ser múltipla a {1}".format(model.referencia.referencia, cantMultiplos)
                return resul
            else:
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
        curLP.setValueBuffer("cantidad", cantidad)
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
        _i = self.iface
        referencia = cursor.valueBuffer("referencia")
        if referencia is None:
            qsatype.FLUtil.ponMsgError("Error: La referencia no existe o no está selecionada")
            return False

        qsatype.FactoriaModulos.get('formRecordpedidoscli').iface.iniciaValoresCursor(cursor)
        if qsatype.FLUtil.sqlSelect(u"articulos", u"sevende", u"referencia = '{}'".format(referencia)) is False:
            qsatype.FLUtil.ponMsgError("Error: El artículo {0} ya no se vende. Selecciona otro.".format(referencia))
            return False
        if not _i.validaCantidadesMultiplos(cursor):
            return False
        return True

    def sanhigia_informes_validaCantidadesMultiplos(self, cursor):
        referencia = cursor.valueBuffer(u"referencia")
        cantidad = cursor.valueBuffer(u"cantidad")
        cantMultiplos = qsatype.FLUtil.sqlSelect(u"articulos", u"sh_canmultiplovta", u"referencia = '{}'".format(referencia))
        if not cantMultiplos or cantMultiplos == u"" or cantMultiplos == 0:
            return True
        if cantidad % cantMultiplos != 0:
            qsatype.FLUtil.ponMsgError(u"La referencia {0} tiene activada la opción múltiplos de cantidad.<br>La cantidad debe ser múltipla a {1}".format(referencia, cantMultiplos))
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

    def validaCantidadesMultiplos(self, cursor):
        return self.ctx.sanhigia_informes_validaCantidadesMultiplos(cursor)

