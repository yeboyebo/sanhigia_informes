
# @class_declaration sanhigia_informes #
from YBUTILS.viewREST import cacheController

class sanhigia_informes(flfacturac):

    def sanhigia_informes_getDesc(self):
        desc = None
        return desc

    def sanhigia_informes_masUno(self, model, oParam):
        _i = self.iface
        idLinea = model.pk
        cantidad = model.cantidad
        cantidad += 1
        response = {}
        if _i.cambiarCantidad(idLinea, cantidad, oParam):
            response["resul"] = True
            response["msg"] = "Cantidad actualizada correctamente"
        else:
            response["status"] = 1
            response["msg"] = "Error actualizando la cantidad"
        return response

    def sanhigia_informes_menosUno(self, model, oParam):
        _i = self.iface
        idLinea = model.pk
        cantidad = model.cantidad
        if cantidad >= 2:
            cantidad -= 1
        else:
            cantidad = 1
        response = {}
        if _i.cambiarCantidad(idLinea, cantidad, oParam):
            response["resul"] = True
            response["msg"] = "Cantidad actualizada correctamente"
        else:
            response["status"] = 1
            response["msg"] = "Error actualizando la cantidad"
        return response

    def sanhigia_informes_modificarCantidad(self, model, oParam):
        _i = self.iface
        idLinea = model.pk
        cantidad = oParam['cantidad']
        return _i.cambiarCantidad(idLinea, cantidad, oParam)

    def sanhigia_informes_cambiarCantidad(self, idLinea, cantidad, oParam):
        # print("____________", oParam)
        curLP = qsatype.FLSqlCursor(u"lineaspedidoscli")
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

        # Esta comentado para que se instale. Cuando se arregla que salga el mensaje se actualizar? Fecha 14-11-2018
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
                    qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.bChCursor("referencia", curLP)
                elif "confirmacion" in oParam and not oParam["confirmacion"]:
                    print("hemos cancelado")
                else:
                    resul = {}
                    resul['status'] = 2
                    resul['confirm'] = "No hay suficiente stock para el artículo " + referencia + " en el almacén " + codAlmacen + ". ¿Desea utilizar su artículo sustitutivo?"
                    resul['oncancel'] = "lanzaraccion"
                    return resul

        qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.bChCursor("cantidad", curLP)
        if not curLP.commitBuffer():
            return False

        return True

    def sanhigia_informes_validateCursor(self, cursor):
        referencia = cursor.valueBuffer("referencia")
        if referencia is None:
            qsatype.FLUtil.ponMsgError("Error: La referencia no existe o no está seleccionada")
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
        print("cantidad______validateCursor: ", cantidad)
        print("disponible__________validateCursor: ", disponible)
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

    def sanhigia_informes_cambiarPrecio(self, model, oParam):
        _i = self.iface
        response = {}
        idLinea = model.pk
        cantidad = model.cantidad
        idPedido = cacheController.getSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()))


        curLP = qsatype.FLSqlCursor(u"lineaspedidoscli")
        curLP.select("idlinea = " + str(idLinea))
        if not curLP.first():
            raise ValueError("Error no se encuentra la linea de pedido ")
            return False
        curLP.setModeAccess(curLP.Edit)
        curLP.refreshBuffer()
        curLP.setActivatedBufferCommited(True)

        curLP.setValueBuffer("dtopor", oParam['dtopor'])

        curLP.setValueBuffer(u"pvptotal", qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_commonCalculateField(u"pvptotal", curLP))

        if not curLP.commitBuffer():
            return False

        if not qsatype.FLUtil.sqlSelect(u"lineaspedidoscli", u"idlinea", ustr(u"idpedido = ", idPedido, u" AND dtopor > 0")):
            if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"sh_estadopago", u"", ustr(u"idpedido = ", idPedido)):
                return False
            if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"pda", u"Pendiente", ustr(u"idpedido = ", idPedido)):
                return False
        else:
            if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"sh_estadopago", u"Pte. Validacion promocion", ustr(u"idpedido = ", idPedido)):
                return False
            if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"pda", u"Suspendido", ustr(u"idpedido = ", idPedido)):
                return False
        return True

    def sanhigia_informes_getForeignFields(self, model, template=None):
        fields = []
        print(template)
        if template == "formRecord":
            fields = [
                {'verbose_name': 'titulo', 'func': 'field_titulo'},
                {'verbose_name': 'calcantidad', 'func': 'field_calCantidad'},
                {'verbose_name': 'caltotal', 'func': 'field_calTotal'},
                {'verbose_name': 'rowColor', 'func': 'field_colorRow'}
            ]
        return fields

    def sanhigia_informes_field_titulo(self, model):
        print(model.referencia.referencia)
        return str(model.referencia.referencia) + " - " + str(model.descripcion)

    def sanhigia_informes_field_calCantidad(self, model):
        #print(model.referencia.referencia)
        return str(int(model.cantidad)) + " x " + str(qsatype.FLUtil.formatoMiles(qsatype.FLUtil.roundFieldValue(model.pvpunitario,"lineaspedidoscli", "pvpunitario"))) + " €"

    def sanhigia_informes_field_calTotal(self, model):
        salida = "Total " + str(qsatype.FLUtil.formatoMiles(qsatype.FLUtil.roundFieldValue(model.pvptotal, "lineaspedidoscli", "pvptotal")))
        if model.dtopor != 0:
            salida += " (" + str(qsatype.FLUtil.formatoMiles(qsatype.FLUtil.roundFieldValue(model.dtopor, "lineaspedidoscli", "dtopor"))) + " % dto)"
        return salida

    def sanhigia_informes_field_colorRow(self, model):
        if model.dtopor != 0:
            return "cWarning"
        else:
            return None

    def sanhigia_informes_borrarLineas(self, model, oParam):
        print("borrando lineas")
        response = {}
        response['status'] = 1
        response['return_data'] = False
        if "selecteds" not in oParam or not oParam['selecteds']:
            response['status'] = -1
            response['msg'] = "Debes seleccionar al menos una línea"
            return response
        aChecked = oParam['selecteds'].split(u",")
        if not aChecked[0]:
            response['msg'] = "Error: Selecciona una o más líneas"
            return response
        print("linea: ", aChecked[0])
        for i in range(len(aChecked)):
            print("llega 1")
            cursor = qsatype.FLSqlCursor("lineaspedidoscli")
            cursor.select(ustr("idlinea = ", aChecked[i]))
            print("llega 2")
            cursor.setModeAccess(cursor.Del)
            print("llega 3")
            cursor.refreshBuffer()
            print("llega 4")
            if cursor.first():
                print("llega 5")
                if not cursor.commitBuffer():
                    print("llega 6")
                    return False
            print("llega 7")
        return response

    def sanhigia_informes_copiaLinea(self, model, oParam):
        print("copiando linea")
        _i = self.iface
        response = {}
        idLinea = model.pk
        cantidad = 1
        dto = 100

        curLP = qsatype.FLSqlCursor(u"lineaspedidoscli")
        curLP.select("idlinea = " + str(idLinea))
        if not curLP.first():
            raise ValueError("Error no se encuentra la linea de pedido ")
            return False
        curLP.setModeAccess(curLP.Browse)
        curLP.refreshBuffer()

        if not _i.copiaDatosLinea(curLP):
            return False

        return True

    def sanhigia_informes_copiaDatosLinea(self, curLP):
        _i = self.iface

        curNuevaLP = qsatype.FLSqlCursor(u"lineaspedidoscli")
        curNuevaLP.setModeAccess(curNuevaLP.Insert)
        curNuevaLP.refreshBuffer()

        curNuevaLP.setValueBuffer(u"idpedido", curLP.valueBuffer("idpedido"))
        curNuevaLP.setValueBuffer(u"referencia", curLP.valueBuffer(u"referencia"))
        curNuevaLP.setValueBuffer(u"descripcion", curLP.valueBuffer(u"descripcion"))
        curNuevaLP.setValueBuffer(u"pvpunitario", curLP.valueBuffer(u"pvpunitario"))
        curNuevaLP.setValueBuffer(u"cantidad", 1)
        curNuevaLP.setValueBuffer(u"codimpuesto", curLP.valueBuffer(u"codimpuesto"))
        curNuevaLP.setValueBuffer(u"iva", curLP.valueBuffer(u"iva"))
        curNuevaLP.setValueBuffer(u"recargo", curLP.valueBuffer(u"recargo"))
        curNuevaLP.setValueBuffer(u"irpf", curLP.valueBuffer(u"irpf"))
        curNuevaLP.setValueBuffer(u"dtolineal", curLP.valueBuffer(u"dtolineal"))
        curNuevaLP.setValueBuffer(u"dtopor", 100)
        curNuevaLP.setValueBuffer(u"porcomision", curLP.valueBuffer(u"porcomision"))
        curNuevaLP.setValueBuffer(u"pvpsindto", qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_commonCalculateField(u"pvpsindto", curNuevaLP))
        curNuevaLP.setValueBuffer(u"pvptotal", qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_commonCalculateField(u"pvptotal", curNuevaLP))

        if not curNuevaLP.commitBuffer():
            return False

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

    def cambiarPrecio(self, model, oParam):
        return self.ctx.sanhigia_informes_cambiarPrecio(model, oParam)

    def getForeignFields(self, model, template=None):
        return self.ctx.sanhigia_informes_getForeignFields(model, template)

    def field_titulo(self, model):
        return self.ctx.sanhigia_informes_field_titulo(model)

    def field_calCantidad(self, model):
        return self.ctx.sanhigia_informes_field_calCantidad(model)

    def field_calTotal(self, model):
        return self.ctx.sanhigia_informes_field_calTotal(model)

    def field_colorRow(self, model):
        return self.ctx.sanhigia_informes_field_colorRow(model)

    def borrarLineas(self, model, oParam):
        return self.ctx.sanhigia_informes_borrarLineas(model, oParam)

    def copiaLinea(self, model, oParam):
        return self.ctx.sanhigia_informes_copiaLinea(model, oParam)

    def copiaDatosLinea(self, curLP):
        return self.ctx.sanhigia_informes_copiaDatosLinea(curLP)

