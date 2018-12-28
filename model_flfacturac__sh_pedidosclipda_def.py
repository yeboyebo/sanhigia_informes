# @class_declaration interna #
from YBLEGACY import qsatype
import os
import datetime
# import babel.numbers
# import decimal

class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *
from YBUTILS.viewREST import cacheController
from YBUTILS import notifications
import xml.etree.cElementTree as ET


class sanhigia_informes(interna):

    def sanhigia_informes_initValidation(self, name, data=None):
        response = True
        cacheController.setSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()), data["DATA"]["idpedido"])
        return response

    def sanhigia_informes_getFilters(self, model, name, template=None):
        filters = []
        if name == 'pedidosUsuario':
            usuario = qsatype.FLUtil.nameUser()
            codGrupo = qsatype.FLUtil.sqlSelect(u"flusers", u"idgroup", ustr(u"iduser = '", usuario, u"' AND idgroup = 'Administracion'"))
            if codGrupo:
                return filters
            else:
                codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
                if not codagente:
                    codagente = '-1'
                return [{'criterio': 'codagente__exact', 'valor': codagente}]
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

    def sanhigia_informes_enviarPedidoPDA(self, model, oParam):
        print("hola mundo")
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
                    print("Direccion: ", direccion)
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
            print("Ruta y Fichero: ", fichero)
            xmlArbol.write(fichero)
            oDM = _i.datosConfigMailPDA()
            nombreCorreo = qsatype.FLUtil.sqlSelect(u"factppal_general", u"sh_mailrecepcion", ustr(u"1 = ", 1))
            print("nombreCorreo: ", nombreCorreo)
            # connection = notifications.get_connection("smtp.gmail.com", "sanhigiapedidos@gmail.com", "a3b2z4Z4", "465", "SSL")
            connection = notifications.get_connection(oDM.hostcorreosaliente, oDM.usuariosmtp, oDM.passwordsmtp, oDM.puertosmtp, oDM.tipocxsmtp)
            response = notifications.sendMail(connection, oDM.usuariosmtp, asunto, cuerpo, [nombreCorreo], fichero)

            # response = notifications.sendSisMail(asunto, cuerpo, [nombreCorreo], fichero)
            os.remove(fichero)
            if not qsatype.FLUtil.sqlUpdate(u"sh_pedidosclipda", u"sh_estadopedidopda", u"Enviado", ustr(u"idpedido = ", idPedido)):
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
        q.setFrom(u"sh_pedidosclipda")
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
        q.setFrom(u"sh_lineaspedidosclipda")
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

    def sanhigia_informes_queryGrid_histArticulosCli(self, model):
        idpedido = cacheController.getSessionVariable(ustr(u"sh_pedidocli_", qsatype.FLUtil.nameUser()))
        print("IDPedido: ", idpedido)
        query = {}
        query["tablesList"] = ("articulos,lineaspedidoscli,pedidoscli")
        query["select"] = ("articulos.referencia, articulos.descripcion, MAX(pedidoscli.fecha) as fecha")
        query["from"] = ("articulos INNER JOIN lineaspedidoscli ON articulos.referencia = lineaspedidoscli.referencia INNER JOIN pedidoscli ON lineaspedidoscli.idpedido = pedidoscli.idpedido")
        query["where"] = ("pedidoscli.codcliente = '" + model.codcliente.codcliente + "' AND lineaspedidoscli.idpedido <> '" + ustr(idpedido) + "'")
        query["groupby"] = " articulos.referencia, articulos.descripcion"
        query["orderby"] = "fecha DESC"
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
            print("hostcorreosaliente", oDM.hostcorreosaliente)
            oDM.puertosmtp = q.value("sh_puertosmtp")
            print("puertosmtp", oDM.puertosmtp)
            oDM.tipocxsmtp = q.value("sh_tipocxsmtp")
            print("tipocxsmtp", oDM.tipocxsmtp)
            oDM.tipoautsmtp = q.value("sh_tipoautsmtp")
            print("tipoautsmtp", oDM.tipoautsmtp)
            oDM.usuariosmtp = q.value("sh_usuariosmtp")
            print("usuariosmtp", oDM.usuariosmtp)
            oDM.passwordsmtp = q.value("sh_passwordsmtp")
            print("passwordsmtp", oDM.passwordsmtp)
        return oDM

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

    def enviarPedidoPDA(self, model, oParam):
        return self.ctx.sanhigia_informes_enviarPedidoPDA(model, oParam)

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

    def queryGrid_histArticulosCli(self, model):
        return self.ctx.sanhigia_informes_queryGrid_histArticulosCli(model)

    def field_colorRow(self, model):
        return self.ctx.sanhigia_informes_field_colorRow(model)


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
