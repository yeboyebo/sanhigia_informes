
# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *
from YBUTILS.viewREST import cacheController
from YBUTILS import notifications
import xml.etree.cElementTree as ET
import os
import datetime


class sanhigia_informes(flfacturac):

    def sanhigia_informes_initValidation(self, name, data=None):
        response = True
        cacheController.setSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()), data["DATA"]["idpedido"])
        return response

    def sanhigia_informes_getFilters(self, model, name, template=None):
        filters = []
        if name == 'pedidosUsuario':
            # filters = [{'criterio': 'editable__exact', 'valor': True}]
            filters = [{'criterio': 'idfacturarec__isnull', 'valor': True}]
            usuario = qsatype.FLUtil.nameUser()
            codGrupo = qsatype.FLUtil.sqlSelect(u"flusers", u"idgroup", ustr(u"iduser = '", usuario, u"' AND idgroup = 'Administracion'"))
            if codGrupo:
                filters = []
            else:
                codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
                if not codagente:
                    codagente = '-1'
                filters.append({'criterio': 'codagente__exact', 'valor': codagente})
        return filters

    def sanhigia_informes_getForeignFields(self, model, template=None):
        fields = []
        if template == "master":
            fields = [{'verbose_name': 'rowColor', 'func': 'field_colorRow'}]
        return fields

    def sanhigia_informes_field_colorRow(self, model):
        if model.sh_estadopedidopda == "Enviado":
            return "cSuccess"
        else:
            return None

    def sanhigia_informes_getDesc(self):
        desc = "nombrecliente"
        return desc

    def sanhigia_informes_iniciaValoresCursor(self, cursor=None):
        qsatype.FactoriaModulos.get('formRecordpedidoscli').iface.iniciaValoresCursor(cursor)
        if cursor.valueBuffer("fechasalida") is None:
            cursor.setValueBuffer("fechasalida", cursor.valueBuffer("fecha"))
        cursor.setValueBuffer(u"sh_estadopago", u"Borrador")
        cursor.setValueBuffer(u"sh_ctrlestadoborr", True)
        return True

    def sanhigia_informes_enviarPedidoPDA(self, model, oParam, cursor):
        try:
            response = True
            _i = self.iface
            idPedido = model.idpedido
            xPedido = ET.Element("pedido")
            xCabecera = ET.SubElement(xPedido, "cabecera")
            camposCab = _i.dameCamposCab(idPedido)
            cuerpo = ""
            nombreCliente = None
            total = None
            neto = None
            totaliva = None
            pvpunitario = None
            pvptotal = None
            asunto = "Pedido " + model.codigo
            direccion = " "
            # cuerpo = "<b>El</b> <i>cliente</i> '" + nombreCliente + "'' hizo un pedido por un total de " + total + " euros.<br><br>"
            if model.observaciones:
                cuerpo += "<br><h2>Observaciones: " + ustr(u"", model.observaciones) + "</h2><br>"
            cuerpo += "<table width='700' cellspacing='1' cellpadding='3' border='1'><tr></th><th>Codigo cliente</th><th>Nombre cliente</th><th>Codigo</th><th>Fecha</th><th>Dirección</th></tr><tr align ='center'>"
            for eCampo in camposCab:
                eValor = eCampo.valor
                if type(eCampo.valor) == str:
                    eValor = str(eCampo.valor)
                xCampo = ET.SubElement(xCabecera, ustr(u"", eCampo.nombre))
                if eCampo.nombre == "total":
                    total = ustr(u"", eValor)
                    # total = babel.numbers.format_currency(decimal.Decimal(total), "EUR", locale = 'es_ES')
                if eCampo.nombre == "neto":
                    neto = ustr(u"", eValor)
                    # neto = babel.numbers.format_currency(decimal.Decimal(neto), "EUR", locale = 'es_ES')
                if eCampo.nombre == "totaliva":
                    totaliva = ustr(u"", eValor)
                    # totaliva = babel.numbers.format_currency(decimal.Decimal(totaliva), "EUR", locale = 'es_ES')
                if eValor is None:
                    eValor = ""
                if eCampo.nombre == "codcliente":
                    cuerpo += "<td>" + ustr(u"", eValor) + "</td>"
                if eCampo.nombre == "nombrecliente":
                    nombreCliente = ustr(u"", eValor)
                    cuerpo += "<td>" + nombreCliente + "</td>"
                if eCampo.nombre == "codigo":
                    cuerpo += "<td>" + ustr(u"", eValor) + "</td>"
                if eCampo.nombre == "fecha":
                    fecha = eValor
                    fecha = fecha.strftime("%d/%m/%Y")
                    cuerpo += "<td>" + ustr(u"", fecha) + "</td>"
                if eCampo.nombre == "dirtipovia" and eValor != "":
                    direccion = ustr(u"", eValor)
                if eCampo.nombre == "direccion" and eValor != "":
                    direccion += u" " + ustr(u"", eValor)
                if eCampo.nombre == "dirnum" and eValor != "":
                    direccion += u" " + ustr(u"", eValor)
                if eCampo.nombre == "dirotros" and eValor != "":
                    direccion += u" " + ustr(u"", eValor)
                if eCampo.nombre == "codpostal" and eValor != "":
                    direccion += u"<br/>" + ustr(u"", eValor)
                if eCampo.nombre == "ciudad" and eValor != "":
                    direccion += u" " + ustr(u"", eValor)
                if eCampo.nombre == "provincia" and eValor != "":
                    direccion += u" " + ustr(u"", eValor)
                if eCampo.nombre == "codpais" and eValor != "":
                    direccion += u" " + ustr(u"", eValor)

                if eCampo.nombre == "coddir" and eValor != "":
                    cuerpo += "<td align='left'>" + direccion + "</td>"
                xCampo.text = ustr(u"", eValor)
            xLineas = ET.SubElement(xPedido, "lineas")
            camposLineas = _i.dameCamposLineas(idPedido)
            cuerpo += "</tr><tr><th>Referencia</th><th>Descripción</th><th>Cantidad</th><th>Precio</th><th>Total</th></tr><tr></tr>"
            i = 0
            for eCampoLinea in camposLineas:
                xLinea = ET.SubElement(xLineas, "linea")
                cuerpo += "<tr>"
                for eLinea in eCampoLinea:
                    xCampoLinea = ET.SubElement(xLinea, ustr(u"", eLinea.nombre))
                    if eLinea.valor is None:
                        eLinea.valor = ""
                    xCampoLinea.text = ustr(u"", eLinea.valor)
                    if eLinea.nombre == "referencia":
                        cuerpo += "<td>" + ustr(u"", eLinea.valor) + "</td>"
                    if eLinea.nombre == "descripcion":
                        cuerpo += "<td>" + ustr(u"", eLinea.valor) + "</td>"
                    if eLinea.nombre == "cantidad":
                        cuerpo += "<td align='right'>" + ustr(u"", eLinea.valor) + "</td>"
                    if eLinea.nombre == "pvpunitario":
                        pvpunitario = ustr(u"", eLinea.valor)
                        # pvpunitario = babel.numbers.format_currency(decimal.Decimal(pvpunitario), "EUR", locale='es_ES')
                        cuerpo += "<td align='right'>" + pvpunitario + "</td>"
                    if eLinea.nombre == "pvptotal":
                        pvptotal = ustr(u"", eLinea.valor)
                        # pvptotal = babel.numbers.format_currency(decimal.Decimal(pvptotal), "EUR", locale='es_ES')
                        cuerpo += "<td align='right'>" + pvptotal + "</td>"
                cuerpo += "</tr>"
                i = i + 1
            cuerpo += "<tr><th colspan='2'><th>Neto</th><th>Total IVA</th><th>Total Pedido</th></tr><tr align='right'><td colspan='2'</td><td>" + neto + "</td><td>" + totaliva + "</td><td>" + total + "</td></tr></table>"
            xmlArbol = ET.ElementTree(xPedido)
            xmlArbol = ET.ElementTree(xPedido)
            # xmlArbol.write("/tmp/prueba.xml")
            fichero = "/tmp/" + model.codigo + ".xml"
            # ruta = os.curdir
            # separador = os.sep
            # fichero = ruta + separador + model.codigo + ".xml"
            xmlArbol.write(fichero)
            oDM = _i.datosConfigMailPDA()
            nombreCorreo = qsatype.FLUtil.sqlSelect(u"factppal_general", u"sh_mailrecepcion", ustr(u"1 = ", 1))
            # connection = notifications.get_connection("smtp.gmail.com", "sanhigiapedidos@gmail.com", "a3b2z4Z4", "465", "SSL")
            connection = notifications.get_connection(oDM.hostcorreosaliente, oDM.usuariosmtp, oDM.passwordsmtp, oDM.puertosmtp, oDM.tipocxsmtp)
            response = notifications.sendMail(connection, oDM.usuariosmtp, asunto, cuerpo, [nombreCorreo], fichero)
            # response = notifications.sendSisMail(asunto, cuerpo, [nombreCorreo], fichero)
            os.remove(fichero)
            if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"sh_estadopedidopda", u"Enviado", u"idpedido = {}".format(idPedido)):
                return False
            estadopago = cursor.valueBuffer("sh_estadopago")
            codcliente = cursor.valueBuffer("codcliente")
            if estadopago == "Borrador con promocion":
                estadopago = "Pte. Validacion promocion"
            elif estadopago == "Borrador":
                codPago = cursor.valueBuffer("codpago")
                bloqueaPedido = qsatype.FLUtil.sqlSelect(u"formaspago", u"sh_bloqueopedido", "codpago = '{}'".format(codPago))
                estadopago = u""
                if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"sh_ctrlestadoborr", False, u"idpedido = {}".format(idPedido)):
                    return False
                if qsatype.FactoriaModulos.get('formpedidoscli').iface.esCanario(cursor):
                    estadopago = u"Aplicar código aduanas"
                    if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"sh_ctrlestadoaduanas", True, u"idpedido = {}".format(idPedido)):
                        return False
                if bloqueaPedido:
                    estadopago = u"Forma de pago bloqueada"
                    if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"sh_ctrlestadopagobloque", True, u"idpedido = {}".format(idPedido)):
                        return False
                if codPago and codPago == u"PA":
                    estadopago = u"Pendiente validar PA"
                    if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"sh_ctrlestadovalidarpa", True, u"idpedido = {}".format(idPedido)):
                        return False
                if qsatype.FactoriaModulos.get('formRecordpedidoscli').iface.clienteTienePagosPtes(codcliente) and cursor.valueBuffer("sh_forzardesbloqueopago") is False:
                    estadopago = u"Pagos pendientes"
                    if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"sh_ctrlestadopagospte", True, u"idpedido = {}".format(idPedido)):
                        return False
            if not qsatype.FLUtil.sqlUpdate(u"pedidoscli", u"sh_estadopago", estadopago, u"idpedido = {}".format(idPedido)):
                return False
        except Exception as e:
            print(e)
        return response

    def sanhigia_informes_dameSelectCabXML(self):
        # _i = self.iface
        select = "idpedido,codcliente,nombrecliente,codigo,fecha,totaleuros,dirtipovia,direccion,dirnum,dirotros,codpostal,ciudad,provincia,codpais,numeropedido,codpago,codejercicio,tasaconv,totalivaportes,codfradirecta,codevento,total,idfradirecta,impreso,pesobultos,codagencia,irpf,creadopor,horario,ivaportes,horaalta,observaciones,horamod,servido,porcomision,editable,idpoblacion,codalmacen,coddir,cifnif,idusuariomod,codimpuestoportes,totalrecargo,codagente,totalportes,regimeniva,recfinanciero,pda,totalreportes,neto,reportes,fechaalta,totalirpf,codtrabajador,codserie,apartado,totaliva,idprovincia,netoportes,idusuarioalta,fechamod,codincidencia,canbultos,fechasalida,coddivisa"
        return  select

    def sanhigia_informes_dameCamposCab(self, idPedido):
        _i = self.iface
        aCampos = qsatype.Array()
        aNombre = qsatype.Array()

        q = qsatype.FLSqlQuery()
        select = _i.dameSelectCabXML()
        q.setSelect(select)
        q.setFrom(u"pedidoscli")
        q.setWhere(ustr(u"idpedido = '", idPedido, u"'"))
        if not q.exec_():
            return False
        if q.first():
            aNombre = select.split(",")
            for nombre in aNombre:
                oCampos = qsatype.Object()
                if q.value(nombre) is not None:
                    oCampos.nombre = nombre
                    oCampos.valor = q.value(nombre)
                    aCampos.append(oCampos)
        return aCampos

    def sanhigia_informes_dameSelectLineaXML(self):
        # _i = self.iface
        select = "referencia,descripcion,cantidad,pvpunitario,pvptotal,canpedidorect,irpf,recargo,dtolineal,cerradapda,dtomanual,codimpuesto,horaalta,horamod,cerrada,porcomision,sh_preparacion,idusuariomod,iva,dtopor,codpreparaciondepedido,pvpsindto,shcantalbaran,tipoprecio,fechaalta,idlineakit,shcodcupon,fechamod,idusuarioalta,tarifasanhigia,totalenalbaran,idlineaorigenregalo"
        return select

    def sanhigia_informes_dameCamposLineas(self, idPedido):
        _i = self.iface
        select = _i.dameSelectLineaXML()
        aLineas = qsatype.Array()
        aNombreLinea = qsatype.Array()
        aNombreLinea = select.split(",")
        q = qsatype.FLSqlQuery()
        q.setSelect(select)
        q.setFrom(u"lineaspedidoscli")
        q.setWhere(ustr(u"idpedido = '", idPedido, u"'"))
        if not q.exec_():
            return False
        while q.next():
            aCamposLinea = qsatype.Array()
            for nombreLinea in aNombreLinea:
                oCamposLinea = qsatype.Object()
                if q.value(nombreLinea) is not None:
                    oCamposLinea.nombre = nombreLinea
                    oCamposLinea.valor = q.value(nombreLinea)
                    aCamposLinea.append(oCamposLinea)
            aLineas.append(aCamposLinea)
        return aLineas

    def sanhigia_informes_queryGrid_histArticulosCli(self, model, filters):
        idpedido = cacheController.getSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()))
        query = {}
        query["tablesList"] = ("articulos,lineaspedidoscli,pedidoscli")
        query["select"] = ("articulos.referencia, articulos.descripcion, MAX(pedidoscli.fecha) as fecha")
        query["from"] = ("articulos INNER JOIN lineaspedidoscli ON articulos.referencia = lineaspedidoscli.referencia INNER JOIN pedidoscli ON lineaspedidoscli.idpedido = pedidoscli.idpedido")
        # query["where"] = ("pedidoscli.codcliente = '" + model.codcliente.codcliente + "' AND lineaspedidoscli.idpedido <> '" + ustr(model.idpedido) + "'")
        query["where"] = "pedidoscli.codcliente = '{0}' AND lineaspedidoscli.idpedido <> '{1}' AND articulos.sevende".format(model.codcliente.codcliente, model.idpedido)
        query["groupby"] = " articulos.referencia, articulos.descripcion"
        query["orderby"] = "fecha DESC"
        query["selectcount"] = "count(distinct(articulos.referencia, articulos.descripcion))"
        return query

    def sanhigia_informes_datosConfigMailPDA(self):
        oDM = qsatype.Object()
        q = qsatype.FLSqlQuery()
        q.setSelect("sh_hostcorreosaliente, sh_puertosmtp, sh_tipocxsmtp, sh_tipoautsmtp, sh_usuariosmtp, sh_passwordsmtp")
        q.setFrom(u"factppal_general")
        q.setWhere(u"1 = 1")
        if not q.exec_():
            return False
        if q.first():
            oDM.hostcorreosaliente = q.value("sh_hostcorreosaliente")
            oDM.puertosmtp = q.value("sh_puertosmtp")
            oDM.tipocxsmtp = q.value("sh_tipocxsmtp")
            oDM.tipoautsmtp = q.value("sh_tipoautsmtp")
            oDM.usuariosmtp = q.value("sh_usuariosmtp")
            oDM.passwordsmtp = q.value("sh_passwordsmtp")
        return oDM

    def sanhigia_informes_validateCursor(self, cursor):
        estadoPago = cursor.valueBuffer("sh_estadopago")
        coddir = cursor.valueBuffer("coddir")
        if not coddir:
            qsatype.FLUtil.ponMsgError("El campo Dir. no esta informado. Por favor, selecciona un codigo valido.")
            return False
        if estadoPago is None or estadoPago == u"":
            return True
        elif estadoPago == u"Borrador con promocion":
            if cursor.valueBuffer("observaciones") is None or cursor.valueBuffer("observaciones") == u"":
                qsatype.FLUtil.ponMsgError("Alguna de las líneas tiene aplicada la promoción, debe rellenar las observaciones.")
                return False
        return True

    def sanhigia_informes_drawIf_pedidoscliForm(self, cursor):
        estadopago = cursor.valueBuffer("sh_estadopago")
        if estadopago == u"Borrador" or estadopago == u"Borrador con promocion":
            return True
        return "disabled"

    def sanhigia_informes_eliminarPedido(self, model, oParam, cursor):
        response = {}
        estadopago = cursor.valueBuffer("sh_estadopago")
        codigo = cursor.valueBuffer("codigo")
        idPedido = cursor.valueBuffer("idpedido")
        if estadopago != u"Borrador" and estadopago != u"Borrador con promocion":
            response["resul"] = False
            response["msg"] = "El pedido '{}' no se puede eliminar porque ya está enviado".format(codigo)
            return response
        if "confirmacion" in oParam and oParam["confirmacion"]:
            cursor = qsatype.FLSqlCursor("pedidoscli")
            cursor.select("idpedido = {}".format(idPedido))
            cursor.setModeAccess(cursor.Del)
            cursor.refreshBuffer()
            if cursor.first():
                if not cursor.commitBuffer():
                    return False
                    # if not qsatype.FLUtil.sqlDelete(u"pedidoscli", u"idpedido = {}".format(idPedido)):
                    response["status"] = 1
                    response["msg"] = "No se puedo eliminar el pedido"
                    return response
            response["resul"] = True
            response["return_data"] = False
            response["msg"] = "El pedido '{}' ha sido eliminado".format(codigo)
            return response
        response["status"] = 2
        response["confirm"] = "El pedido '{}' será eliminado.¿Estás seguro?".format(codigo)
        return response

    def sanhigia_informes_drawIf_verSeguimiento(self, cursor):
        return "disabled"

    def sanhigia_informes_visualizarSeguimiento(self, model):
        _i = self.iface
        idpedido = model.idpedido
        codigo = model.codigo
        fecha = model.fecha
        fecha = fecha.strftime('%d - %m - %Y')
        nombrecliente = model.nombrecliente
        response = {}
        oSeguimientos = []
        oSeguimientos = _i.dameObjetoSeguimientos(idpedido)
        if oSeguimientos is False:
            resul = {}
            resul['status'] = -1
            resul['msg'] = "No existe número tracking para el albarán asociado al pedido {}".format(codigo)
            return resul
        if len(oSeguimientos) == 1:
            oSeguimientos[0]["urlsegui"] = oSeguimientos[0]["urlsegui"].replace("#TN#", oSeguimientos[0]["numtracking"])
            response["url"] = oSeguimientos[0]["urlsegui"]
            response["newtab"] = True
            return response

        response["status"] = 2
        response["confirm"] = "<div  style='overflow:hidden;''><div style='position:relative;float:left;'><div>Pedido " + codigo + "</div><br><table>"
        response["customButtons"] = []
        for oSegui in oSeguimientos:
            oSegui["urlsegui"] = oSegui["urlsegui"].replace("#TN#", oSegui["numtracking"])
            response["confirm"] += "<tr style='padding-top:10'><td style=''>Cod.Albarán - " + oSegui["codalbaran"] + "</td></tr><tr><td style=''>Agencia - " + oSegui["codagencia"] + "</td></tr><tr><td><a href='" + oSegui["urlsegui"] + "' target='_blank'>Ver Seguimiento - " + oSegui["numtracking"] + "</a></td></tr><tr><td><br></td></tr>"
        response["confirm"] += "</table>"
        return response

    def sanhigia_informes_dameObjetoSeguimientos(self, idpedido):
        oSeguimientos = []
        q = qsatype.FLSqlQuery()
        q.setTablesList(u"albaranescli,lineasalbaranescli,pedidoscli,agenciastrans")
        q.setSelect(u"a.codigo,a.sh_numtracking,a.codagencia,at.urlsegui")
        q.setFrom(u"albaranescli a INNER JOIN lineasalbaranescli la ON a.idalbaran = la.idalbaran INNER JOIN pedidoscli p ON la.idpedido = p.idpedido INNER JOIN agenciastrans at ON a.codagencia = at.codagencia")
        q.setWhere(u"p.idpedido = {} AND a.sh_numtracking IS NOT NULL GROUP BY a.codigo, a.sh_numtracking,a.codagencia,at.urlsegui ORDER BY a.codigo".format(idpedido))
        if not q.exec_():
            return False
        if q.size() == 0:
            return False
        while q.next():
            oSeguimiento = {}
            oSeguimiento["codalbaran"] = q.value("a.codigo")
            oSeguimiento["numtracking"] = q.value("a.sh_numtracking")
            oSeguimiento["urlsegui"] = q.value("at.urlsegui")
            oSeguimiento["codagencia"] = q.value("a.codagencia")
            oSeguimientos.append(oSeguimiento)
        return oSeguimientos

    def sanhigia_informes_drawIf_deshabilitarCampos(self, cursor):
        usuario = qsatype.FLUtil.nameUser()
        codGrupo = qsatype.FLUtil.sqlSelect(u"flusers", u"idgroup", ustr(u"iduser = '", usuario, u"' AND idgroup = 'Administracion'"))
        if not codGrupo:
            return "disabled"

    def __init__(self, context=None):
        super().__init__(context)

    def initValidation(self, name, data=None):
        return self.ctx.sanhigia_informes_initValidation(name, data)

    def getFilters(self, model, name, template=None):
        return self.ctx.sanhigia_informes_getFilters(model, name, template)

    def getForeignFields(self, model, template=None):
        return self.ctx.sanhigia_informes_getForeignFields(model, template)

    def getDesc(self):
        return self.ctx.sanhigia_informes_getDesc()

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.sanhigia_informes_iniciaValoresCursor(cursor)

    def enviarPedidoPDA(self, model, oParam, cursor):
        return self.ctx.sanhigia_informes_enviarPedidoPDA(model, oParam, cursor)

    def dameCamposCab(self, idPedido):
        return self.ctx.sanhigia_informes_dameCamposCab(idPedido)

    def dameSelectCabXML(self):
        return self.ctx.sanhigia_informes_dameSelectCabXML()

    def dameCamposLineas(self, idPedido):
        return self.ctx.sanhigia_informes_dameCamposLineas(idPedido)

    def datosConfigMailPDA(self, ):
        return self.ctx.sanhigia_informes_datosConfigMailPDA()

    def dameSelectLineaXML(self):
        return self.ctx.sanhigia_informes_dameSelectLineaXML()

    def queryGrid_histArticulosCli(self, model, filters):
        return self.ctx.sanhigia_informes_queryGrid_histArticulosCli(model, filters)

    def field_colorRow(self, model):
        return self.ctx.sanhigia_informes_field_colorRow(model)

    def validateCursor(self, cursor):
        return self.ctx.sanhigia_informes_validateCursor(cursor)

    def drawIf_pedidoscliForm(self, cursor):
        return self.ctx.sanhigia_informes_drawIf_pedidoscliForm(cursor)

    def eliminarPedido(self, model, oParam, cursor):
        return self.ctx.sanhigia_informes_eliminarPedido(model, oParam, cursor)

    def drawIf_verSeguimiento(self, cursor):
        return self.ctx.sanhigia_informes_drawIf_verSeguimiento(cursor)

    def visualizarSeguimiento(self, model):
        return self.ctx.sanhigia_informes_visualizarSeguimiento(model)

    def dameObjetoSeguimientos(self, idpedido):
        return self.ctx.sanhigia_informes_dameObjetoSeguimientos(idpedido)

    def drawIf_deshabilitarCampos(self, cursor):
        return self.ctx.sanhigia_informes_drawIf_deshabilitarCampos(cursor)

