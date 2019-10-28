
# @class_declaration sanhigia_informes #
from YBUTILS.viewREST import cacheController


class sanhigia_informes(flfactalma):

    def sanhigia_informes_getReferenciaDesc(self, model, oParam):
        data = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"articulos")
        q.setSelect(u"referencia,descripcion")
        q.setFrom(u"articulos")
        q.setWhere(u"(UPPER(referencia) LIKE '%" + oParam['val'].upper() + "%' OR UPPER(descripcion) LIKE '%" + oParam['val'].upper() + "%') AND sevende = true")
        # q.setWhere(u"(UPPER(referencia) LIKE '%" + oParam['val'].upper() + "%' OR UPPER(descripcion) LIKE '%" + oParam['val'].upper() + "%')")
        if not q.exec_():
            print("Error inesperado")
            return []
        if q.size() > 200:
            return []
        while q.next():
            descripcion = str(q.value(0)) + "  " + q.value(1)
            data.append({"descripcion": descripcion, "referencia": q.value(0)})
        return data

    def sanhigia_informes_subirLinea(self, model, oParam, cursor):
        response = True
        _i = self.iface
        print("algo", oParam)
        idpedido = cacheController.getSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()))
        estadopago = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"sh_estadopago", u"idpedido = {}".format(idpedido))
        if estadopago != u"Borrador" and estadopago != u"Borrador con promocion":
            resul = {}
            resul['status'] = -1
            resul['msg'] = "La referencia no se puede añadir. El pedido ya está enviado"
            return resul
        print(idpedido)
        referencia = qsatype.FLUtil.sqlSelect(u"lineaspedidoscli", u"referencia", ustr(u"referencia = '", model.referencia, u"' AND idpedido = '", idpedido, u"'"))
        cantidad = qsatype.FLUtil.sqlSelect(u"lineaspedidoscli", u"cantidad", ustr(u"referencia = '", model.referencia, u"' AND idpedido = '", idpedido, u"'"))
        # cantidad = qsatype.FLUtil.sqlSelect(u"sh_lineaspedidosclipda", u"cantidad", ustr(u"referencia = '", model.referencia, u"' AND idpedido = '", idpedido, u"'"))
        if referencia:
            resul = {}
            resul['status'] = -1
            resul['msg'] = "Error: La referencia ya esta en el pedido"
            return resul
        else:
            # TODO Comprobar stocks
            referencia = cursor.valueBuffer("referencia")
            codAlmacen = "ALM"
            # qsatype.FLUtil.sqlSelect(u"pedidoscli", u"codalmacen", ustr(u"idpedido = ", idpedido))
            cantidad = 1
            disponible = qsatype.FLUtil.sqlSelect(u"stocks", u"disponible", ustr(u"referencia = '", referencia, u"' AND codalmacen = '", codAlmacen, u"'"))
            if cantidad > disponible:
                if qsatype.FLUtil.sqlSelect(u"articulos", u"referencia", ustr(u"refsustitutivo = '", referencia, u"'")):
                    print("sale por aqui")
                    _i.insertarLinea(cursor, oParam)
                    return response
                refSust = qsatype.FLUtil.sqlSelect(u"articulos", u"refsustitutivo", ustr(u"referencia = '", referencia, u"'"))
                if not refSust or refSust == u"":
                    return _i.insertarLinea(cursor, oParam)
                if "confirmacion" in oParam and oParam["confirmacion"]:
                    curArticulo = qsatype.FLSqlCursor(u"articulos")
                    curArticulo.select(ustr(u"referencia = '", refSust, u"'"))
                    if not curArticulo.first():
                        return False
                    curArticulo.setModeAccess(curArticulo.Browse)
                    curArticulo.refreshBuffer()
                    return _i.insertarLinea(curArticulo, oParam)
                else:
                    response = {}
                    response["status"] = 2
                    response["confirm"] = "No hay suficiente stock para el artículo " + referencia + " en el almacén " + codAlmacen + ". ¿Desea utilizar su artículo sustitutivo?"
                    return response
            # if not qsatype.FLUtil.sqlSelect(u"articulos", u"referencia", ustr(u"refsustitutivo = '", referencia, u"'")):
            #     refSust = qsatype.FLUtil.sqlSelect(u"articulos", u"refsustitutivo", ustr(u"referencia = '", referencia, u"'"))
            #     cantidad = parseFloat(curL.valueBuffer(u"cantidad"))
            #     disponible = qsatype.FLUtil.sqlSelect(u"stocks", u"disponible", ustr(u"referencia = '", referencia, u"' AND codalmacen = '", codAlmacen, u"'"))
            #     if cantidad > disponible:
            #         return refSust
            _i.insertarLinea(cursor, oParam)
            '''
            curPedido = qsatype.FLSqlCursor(u"sh_pedidosclipda")
            curPedido.select(ustr(u"idpedido = ", idpedido))
            if not qsatype.FactoriaModulos.get('formRecordsh_pedidosclipda').iface.calcularTotalesCursor(curPedido):
                return False
            '''
        print("sale por aqui???")
        return response

    def sanhigia_informes_insertarLinea(self, cursor, oParam):
        # _i = self.iface
        idpedido = cacheController.getSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()))
        curLinea = qsatype.FLSqlCursor(u"lineaspedidoscli")
        curLinea.setModeAccess(curLinea.Insert)
        curLinea.refreshBuffer()
        curLinea.setActivatedBufferCommited(True)
        curLinea.setValueBuffer(u"idpedido", idpedido)
        curLinea.setValueBuffer(u"referencia", cursor.valueBuffer("referencia"))
        curLinea.setValueBuffer(u"descripcion", cursor.valueBuffer("descripcion"))
        curLinea.setValueBuffer(u"codimpuesto", qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_commonCalculateField(u"codimpuesto", curLinea))
        curLinea.setValueBuffer(u"iva", qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_commonCalculateField(u"iva", curLinea))
        #curLinea.setValueBuffer(u"cantidad", model.cantidad)
        curLinea.setValueBuffer(u"cantidad", 1)
        curLinea.setValueBuffer(u"pvpunitario", qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_commonCalculateField(u"pvpunitario", curLinea))
        curLinea.setValueBuffer(u"pvpsindto", qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_commonCalculateField(u"pvpsindto", curLinea))
        curLinea.setValueBuffer(u"pvptotal", qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_commonCalculateField(u"pvptotal", curLinea))
        curLinea.setValueBuffer(u"porcomision", qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_commonCalculateField(u"porcomision", curLinea))
        curLinea.setValueBuffer(u"recargo", qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_commonCalculateField(u"recargo", curLinea) or 0)
        if not curLinea.commitBuffer():
            return False
        return True

    def sanhigia_informes_subirLineaPres(self, model, oParam, cursor):
        response = True
        _i = self.iface
        idpresupuesto = cacheController.getSessionVariable(ustr(u"presupuestoscli_", qsatype.FLUtil.nameUser()))
        print(idpresupuesto)
        referencia = qsatype.FLUtil.sqlSelect(u"lineaspresupuestoscli", u"referencia", ustr(u"referencia = '", model.referencia, u"' AND idpresupuesto = '", idpresupuesto, u"'"))
        cantidad = qsatype.FLUtil.sqlSelect(u"lineaspresupuestoscli", u"cantidad", ustr(u"referencia = '", model.referencia, u"' AND idpresupuesto = '", idpresupuesto, u"'"))
        if referencia:
            resul = {}
            resul['status'] = -1
            resul['msg'] = "Error: La referencia ya esta en el presupuesto"
            return resul
        else:
            # TODO Comprobar stocks
            referencia = cursor.valueBuffer("referencia")
            # codAlmacen = qsatype.FLUtil.sqlSelect(u"presupuestoscli", u"codalmacen", ustr(u"idpresupuesto = '", idpresupuesto, u"'"))
            codAlmacen = "ALM"
            cantidad = 1
            disponible = qsatype.FLUtil.sqlSelect(u"stocks", u"disponible", ustr(u"referencia = '", referencia, u"' AND codalmacen = '", codAlmacen, u"'"))
            if disponible == None:
                disponible = 0
            if cantidad > disponible:
                if qsatype.FLUtil.sqlSelect(u"articulos", u"referencia", ustr(u"refsustitutivo = '", referencia, u"'")):
                    print("sale por aqui")
                    return False
                refSust = qsatype.FLUtil.sqlSelect(u"articulos", u"refsustitutivo", ustr(u"referencia = '", referencia, u"'"))
                if not refSust or refSust == u"":
                    return _i.insertarLineaPres(cursor, oParam)
                if "confirmacion" in oParam and oParam["confirmacion"]:
                    curArticulo = qsatype.FLSqlCursor(u"articulos")
                    curArticulo.select(ustr(u"referencia = '", refSust, u"'"))
                    if not curArticulo.first():
                        return False
                    curArticulo.setModeAccess(curArticulo.Browse)
                    curArticulo.refreshBuffer()
                    return _i.insertarLineaPres(curArticulo, oParam)
                else:
                    response = {}
                    response["status"] = 2
                    response["confirm"] = "No hay suficiente stock para el artículo " + referencia + " en el almacén " + codAlmacen + ". ¿Desea utilizar su artículo sustitutivo?"
                    return response
            # if not qsatype.FLUtil.sqlSelect(u"articulos", u"referencia", ustr(u"refsustitutivo = '", referencia, u"'")):
            #     refSust = qsatype.FLUtil.sqlSelect(u"articulos", u"refsustitutivo", ustr(u"referencia = '", referencia, u"'"))
            #     cantidad = parseFloat(curL.valueBuffer(u"cantidad"))
            #     disponible = qsatype.FLUtil.sqlSelect(u"stocks", u"disponible", ustr(u"referencia = '", referencia, u"' AND codalmacen = '", codAlmacen, u"'"))
            #     if cantidad > disponible:
            #         return refSust
            _i.insertarLineaPres(cursor, oParam)
            '''
            curPedido = qsatype.FLSqlCursor(u"sh_pedidosclipda")
            curPedido.select(ustr(u"idpedido = ", idpedido))
            if not qsatype.FactoriaModulos.get('formRecordsh_pedidosclipda').iface.calcularTotalesCursor(curPedido):
                return False
            '''
        print("sale por aqui???")
        return response

    def sanhigia_informes_insertarLineaPres(self, cursor, oParam):
        # _i = self.iface
        idpresupuesto = cacheController.getSessionVariable(ustr(u"presupuestoscli_", qsatype.FLUtil.nameUser()))
        curLinea = qsatype.FLSqlCursor(u"lineaspresupuestoscli")
        curLinea.setModeAccess(curLinea.Insert)
        curLinea.refreshBuffer()
        curLinea.setActivatedBufferCommited(True)
        curLinea.setValueBuffer(u"idpresupuesto", idpresupuesto)
        curLinea.setValueBuffer(u"referencia", cursor.valueBuffer("referencia"))
        curLinea.setValueBuffer(u"descripcion", cursor.valueBuffer("descripcion"))
        curLinea.setValueBuffer(u"codimpuesto", qsatype.FactoriaModulos.get('formRecordlineaspresupuestoscli').iface.commonCalculateField(u"codimpuesto", curLinea))
        curLinea.setValueBuffer(u"iva", qsatype.FactoriaModulos.get('formRecordlineaspresupuestoscli').iface.commonCalculateField(u"iva", curLinea))
        #curLinea.setValueBuffer(u"cantidad", model.cantidad)
        curLinea.setValueBuffer(u"cantidad", 1)
        curLinea.setValueBuffer(u"pvpunitario", qsatype.FactoriaModulos.get('formRecordlineaspresupuestoscli').iface.commonCalculateField(u"pvpunitario", curLinea))
        curLinea.setValueBuffer(u"pvpsindto", qsatype.FactoriaModulos.get('formRecordlineaspresupuestoscli').iface.commonCalculateField(u"pvpsindto", curLinea))
        curLinea.setValueBuffer(u"pvptotal", qsatype.FactoriaModulos.get('formRecordlineaspresupuestoscli').iface.commonCalculateField(u"pvptotal", curLinea))
        curLinea.setValueBuffer(u"porcomision", qsatype.FactoriaModulos.get('formRecordlineaspresupuestoscli').iface.commonCalculateField(u"porcomision", curLinea))
        curLinea.setValueBuffer(u"recargo", qsatype.FactoriaModulos.get('formRecordlineaspresupuestoscli').iface.commonCalculateField(u"recargo", curLinea) or 0)
        if not curLinea.commitBuffer():
            return False
        return True

    def __init__(self, context=None):
        super().__init__(context)

    def getReferenciaDesc(self, model, oParam):
        return self.ctx.sanhigia_informes_getReferenciaDesc(model, oParam)

    def subirLinea(self, model, oParam, cursor):
        return self.ctx.sanhigia_informes_subirLinea(model, oParam, cursor)

    def insertarLinea(self, cursor, oParam):
        return self.ctx.sanhigia_informes_insertarLinea(cursor, oParam)

    def subirLineaPres(self, model, oParam, cursor):
        return self.ctx.sanhigia_informes_subirLineaPres(model, oParam, cursor)

    def insertarLineaPres(self, cursor, oParam):
        return self.ctx.sanhigia_informes_insertarLineaPres(cursor, oParam)

