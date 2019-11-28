
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
        idPedido = cacheController.getSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()))
        estadopago = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"sh_estadopago", u"idpedido = {}".format(idPedido))
        if estadopago != u"Borrador" and estadopago != u"Borrador con promocion":
            response["resul"] = -1
            response["msg"] = "La linea no se puede modificar. El pedido ya está enviado"
            return response
        response = _i.cambiarCantidad(idLinea, cantidad, oParam)
        return response

    def sanhigia_informes_menosUno(self, model, oParam):
        _i = self.iface
        idLinea = model.pk
        cantidad = model.cantidad
        response = {}
        idPedido = cacheController.getSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()))
        estadopago = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"sh_estadopago", u"idpedido = {}".format(idPedido))
        if estadopago != u"Borrador" and estadopago != u"Borrador con promocion":
            response["resul"] = -1
            response["msg"] = "La linea no se puede modificar. El pedido ya está enviado"
            return response
        if cantidad >= 2:
            cantidad -= 1
        else:
            cantidad = 1
        response = _i.cambiarCantidad(idLinea, cantidad, oParam)
        return response

    def sanhigia_informes_modificarCantidad(self, model, oParam):
        _i = self.iface
        idLinea = model.pk
        cantidad = oParam['cantidad']
        response = {}
        idPedido = cacheController.getSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()))
        estadopago = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"sh_estadopago", u"idpedido = {}".format(idPedido))
        if estadopago != u"Borrador" and estadopago != u"Borrador con promocion":
            response["resul"] = -1
            response["msg"] = "La linea no se puede modificar. El pedido ya está enviado"
            return response
        return _i.cambiarCantidad(idLinea, cantidad, oParam)

    def sanhigia_informes_cambiarCantidad(self, idLinea, cantidad, oParam):
        response = {}
        haystock = True
        haystockSust = True
        curLP = qsatype.FLSqlCursor(u"lineaspedidoscli")
        curLP.select("idlinea = " + str(idLinea))
        if not curLP.first():
            raise ValueError("Error no se encuentra la linea de pedido ")
            return False
        curLP.setModeAccess(curLP.Edit)
        curLP.refreshBuffer()
        curLP.setActivatedBufferCommited(True)
        curLP.setValueBuffer("cantidad", cantidad)
        referencia = curLP.valueBuffer("referencia")
        codAlmacen = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"codalmacen", u"idpedido = {}".format(curLP.valueBuffer("idpedido")))
        disponible = qsatype.FLUtil.sqlSelect(u"stocks", u"disponible", u"referencia = '{0}' AND codalmacen = '{1}'".format(referencia, codAlmacen))
        if not disponible:
            disponible = 0
        if disponible <= 0 or parseFloat(cantidad) > parseFloat(disponible):
            haystock = False
            refSust = qsatype.FLUtil.sqlSelect(u"articulos", u"refsustitutivo", u"referencia = '{}'".format(referencia))
            if refSust and refSust != u"":
                disponibleSust = qsatype.FLUtil.sqlSelect(u"stocks", u"disponible", u"referencia = '{0}' AND codalmacen = '{1}'".format(refSust, codAlmacen))
                if disponibleSust <= 0 or parseFloat(cantidad) > parseFloat(disponibleSust):
                    haystockSust = False
                else:
                    descripcionSust = qsatype.FLUtil.sqlSelect(u"articulos", u"descripcion", u"referencia = '{}'".format(refSust))
                    curLP.setValueBuffer("referencia", refSust)
                    curLP.setValueBuffer("descripcion", descripcionSust)
        if haystock:
            qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.bChCursor("cantidad", curLP)
            if not curLP.commitBuffer():
                response["msg"] = "Error al guardar los cambios"
                response["resul"] = -1
            else:
                response["msg"] = "Cantidad actualizada correctamente"
                response["resul"] = 1

        elif haystockSust:
            qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.bChCursor("cantidad", curLP)
            if not curLP.commitBuffer():
                response["msg"] = "Error al guardar los cambios"
                response["resul"] = -1
            else:
                # response["msg"] = mensaje + "\nCantidad actualizada correctamente"
                response["msg"] = "Se ha cambiado la referencia {0} con su artículo sustitutivo {1}.\nCantidad actualizada correctamente".format(referencia, refSust)
                response["resul"] = 1
        else:
            response["msg"] = "No hay suficiente stock para el artículo {0} y su sustitutivo {1}.\nPor favor, selecciona otro artículo o cambie la cantidad.".format(referencia, refSust)
            response["resul"] = -1
        return response

    def sanhigia_informes_validateCursor(self, cursor):
        referencia = cursor.valueBuffer("referencia")
        if referencia is None:
            qsatype.FLUtil.ponMsgError("Error: La referencia no existe o no está seleccionada")
            return False
        if qsatype.FLUtil.sqlSelect(u"articulos", u"sevende", u"referencia = '{}'".format(referencia)) is False:
            qsatype.FLUtil.ponMsgError("Error: El artículo {0} ya no se vende.\nPor favor, selecciona otro.".format(referencia))
            return False
        codAlmacen = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"codalmacen", u"idpedido = {}".format(cursor.valueBuffer("idpedido")))
        cantidad = parseFloat(cursor.valueBuffer("cantidad"))
        disponible = qsatype.FLUtil.sqlSelect(u"stocks", u"disponible", u"referencia = '{0}' AND codalmacen = '{1}'".format(referencia, codAlmacen))
        if not disponible:
            disponible = 0
        if cantidad > parseFloat(disponible):
            refSust = qsatype.FLUtil.sqlSelect(u"articulos", u"refsustitutivo", u"referencia = '{}'".format(referencia))
            if not refSust or refSust == u"":
                qsatype.FLUtil.ponMsgError("Para la referencia {0} no existe ningún artículo sustitutivo disponible.\nPor favor, selecciona otro artículo.".format(referencia))
                return False
            disponibleSust = qsatype.FLUtil.sqlSelect(u"stocks", u"disponible", u"referencia = '{0}' AND codalmacen = '{1}'".format(refSust, codAlmacen))
            if disponibleSust <= 0 or cantidad > parseFloat(disponibleSust):
                qsatype.FLUtil.ponMsgError("No hay suficiente stock para el artículo {0} y su sustitutivo {1}.\nPor favor, selecciona otro artículo o cambie la cantidad.".format(referencia, refSust))
                return False
            # Lo comento porque no me sale el toast de aviso de cambio con el sustitutivo
            # qsatype.FLUtil.ponMsgError("Se ha cambiado la referencia {0} con su artículo sustitutivo {1}.".format(referencia, refSust))
            # return True
            # qsatype.FactoriaModulos.get('flfacturac').iface.pub_establecerSustitutivo(cursor, refSust)
            descripcionSust = qsatype.FLUtil.sqlSelect(u"articulos", u"descripcion", u"referencia = '{}'".format(refSust))
            cursor.setValueBuffer("referencia", refSust)
            cursor.setValueBuffer("descripcion", descripcionSust)
            resul = {}
            resul["resul"] = {}
            resul["resul"]['status'] = 2
            resul["resul"]['confirm'] = "No hay suficiente stock para el artículo {0} en el almacén {1}. ¿Desea utilizar su artículo sustitutivo {2}?".format(referencia, codAlmacen, refSust)
            resul["resul"]['onconfirm'] = "changedata"
            return resul
        return True

    def sanhigia_informes_cambiarPrecio(self, model, oParam):
        response = {}
        idLinea = model.pk
        # idLinea = model.idlinea.referencia
        idPedido = cacheController.getSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()))
        estadopago = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"sh_estadopago", u"idpedido = {}".format(idPedido))
        if estadopago != u"Borrador" and estadopago != u"Borrador con promocion":
            response["resul"] = -1
            response["msg"] = "La linea no se puede modificar. El pedido ya está enviado"
            return response
        curLP = qsatype.FLSqlCursor(u"lineaspedidoscli")
        curLP.select("idlinea = " + str(idLinea))
        if not curLP.first():
            raise ValueError("Error no se encuentra la linea de pedido ")
            return False
        curLP.setModeAccess(curLP.Edit)
        curLP.refreshBuffer()
        curLP.setActivatedBufferCommited(True)
        curLP.setValueBuffer("dtomanual", True)
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
            if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"sh_estadopago", u"Borrador con promocion", ustr(u"idpedido = ", idPedido)):
                return False
            if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"pda", u"Suspendido", ustr(u"idpedido = ", idPedido)):
                return False
        return True

    def sanhigia_informes_getForeignFields(self, model, template=None):
        fields = []
        if template == "formRecord":
            fields = [
                {'verbose_name': 'titulo', 'func': 'field_titulo'},
                {'verbose_name': 'calcantidad', 'func': 'field_calCantidad'},
                {'verbose_name': 'caltotal', 'func': 'field_calTotal'},
                {'verbose_name': 'rowColor', 'func': 'field_colorRow'}
            ]
        return fields

    def sanhigia_informes_field_titulo(self, model):
        return str(model.referencia.referencia) + " - " + str(model.descripcion)

    def sanhigia_informes_field_calCantidad(self, model):
        return str(int(model.cantidad)) + " x " + str(qsatype.FLUtil.formatoMiles(qsatype.FLUtil.roundFieldValue(model.pvpunitario, "lineaspedidoscli", "pvpunitario"))) + " €"

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
        response = {}
        idPedido = cacheController.getSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()))
        estadopago = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"sh_estadopago", u"idpedido = {}".format(idPedido))
        if estadopago != u"Borrador" and estadopago != u"Borrador con promocion":
            response["status"] = -1
            response["msg"] = "La linea no se puede borrar. El pedido ya está enviado"
            return response
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
        for i in range(len(aChecked)):
            cursor = qsatype.FLSqlCursor("lineaspedidoscli")
            cursor.select(ustr("idlinea = ", aChecked[i]))
            cursor.setModeAccess(cursor.Del)
            cursor.refreshBuffer()
            if cursor.first():
                if not cursor.commitBuffer():
                    return False
        idPedido = cacheController.getSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()))
        curPedido = qsatype.FLSqlCursor(u"pedidoscli")
        curPedido.select(ustr(u"idpedido = ", idPedido))
        if not curPedido.first():
            return False
        curPedido.setModeAccess(curPedido.Edit)
        curPedido.refreshBuffer()
        if not qsatype.FactoriaModulos.get('formRecordpedidoscli').iface.calcularTotalesCursor(curPedido):
            return False
        if not curPedido.commitBuffer():
            return False
        return response

    def sanhigia_informes_copiaLinea(self, model, oParam):
        _i = self.iface
        idLinea = model.pk
        idPedido = cacheController.getSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()))
        estadopago = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"sh_estadopago", u"idpedido = {}".format(idPedido))
        if estadopago != u"Borrador" and estadopago != u"Borrador con promocion":
            resul = {}
            resul['status'] = -1
            resul['msg'] = "La linea no se puede copiar. El pedido ya está enviado"
            return resul
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
        curNuevaLP.setValueBuffer(u"dtomanual", True)
        curNuevaLP.setValueBuffer(u"dtopor", 100)
        curNuevaLP.setValueBuffer(u"porcomision", curLP.valueBuffer(u"porcomision"))
        curNuevaLP.setValueBuffer(u"pvpsindto", qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_commonCalculateField(u"pvpsindto", curNuevaLP))
        curNuevaLP.setValueBuffer(u"pvptotal", qsatype.FactoriaModulos.get('formRecordlineaspedidoscli').iface.pub_commonCalculateField(u"pvptotal", curNuevaLP))

        if not curNuevaLP.commitBuffer():
            return False

        # if not qsatype.FLUtil.sqlSelect(u"lineaspedidoscli", u"idlinea", ustr(u"idpedido = ", idPedido, u" AND dtopor > 0")):
        #     if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"sh_estadopago", u"", ustr(u"idpedido = ", idPedido)):
        #         return False
        #     if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"pda", u"Pendiente", ustr(u"idpedido = ", idPedido)):
        #         return False
        # else:
        if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"sh_estadopago", u"Borrador con promocion", u"idpedido = {}".format(curLP.valueBuffer("idpedido"))):
            return False
        if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"pda", u"Suspendido", u"idpedido = {}".format(curLP.valueBuffer("idpedido"))):
            return False

        return True

    def sanhigia_informes_drawIf_lineaspedidoscliForm(self, cursor):
        estadopago = qsatype.FLUtil.sqlSelect(u"pedidoscli", u"sh_estadopago", u"idpedido = {}".format(cursor.valueBuffer("idpedido")))
        if estadopago == u"Borrador" or estadopago == u"Borrador con promocion":
            return True
        return "disabled"

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

    def drawIf_lineaspedidoscliForm(self, cursor):
        return self.ctx.sanhigia_informes_drawIf_lineaspedidoscliForm(cursor)

