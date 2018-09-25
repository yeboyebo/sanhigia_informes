# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *
from models.flfactppal.agentes import agentes

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
        if name == 'filtroagente':
            usr = qsatype.FLUtil.nameUser()
            if usr != "infosial" and usr != "jesus":
                agente = agentes.objects.filter(idusuario__exact=usr)
                return [{'criterio': 'i_facturascli_codagente__in', 'valor': [agente[0].codagente]}]
        return filters

    def sanhigia_informes_getForeignFields(self, model, template=None):
        fields = []
        if template == 'master':
            return [
                {'verbose_name': 'nombreagente', 'func': 'field_nombreagente'}
            ]
        return fields

    def field_nombreagente(self, model):
        return self.ctx.sanhigia_field_nombreagente(model)

    def sanhigia_informes_getDesc(self):
        desc = None
        return desc

    def sanhigia_report_consumocliente(self, model):
        qry = {}
        qry['select'] = " empresa.nombre, empresa.cifnif, empresa.direccion, empresa.codpostal, empresa.ciudad, empresa.provincia, facturascli.codcliente, facturascli.nombrecliente, facturascli.cifnif, facturascli.codigo, facturascli.fecha, facturascli.direccion, facturascli.codpostal, facturascli.ciudad, facturascli.provincia,"
        qry['select'] += " lineasfacturascli.referencia, lineasfacturascli.descripcion, lineasfacturascli.cantidad, lineasfacturascli.pvptotal, lineasfacturascli.pvpunitario, i_sh_consumocliente.d_facturascli_fecha, i_sh_consumocliente.h_facturascli_fecha, i_sh_consumocliente.i_facturascli_codagente, agentes.nombreap"

        qry['from'] = " empresa, i_sh_consumocliente LEFT JOIN agentes ON i_sh_consumocliente.i_facturascli_codagente = agentes.codagente, lineasfacturascli INNER JOIN facturascli ON lineasfacturascli.idfactura = facturascli.idfactura INNER JOIN clientes ON facturascli.codcliente = clientes.codcliente"
        qry['where'] = ""
        qry['where'] += " i_sh_consumocliente.id = " + str(model.id) if qry['where'] == "" else " AND i_sh_consumocliente.id = " + str(model.id) if model.id else ""
        qry['where'] += " facturascli.codcliente = '" + str(model.i_facturascli_codcliente) + "'" if qry['where'] == "" else " AND facturascli.codcliente = '" + str(model.i_facturascli_codcliente) + "'" if model.i_facturascli_codcliente else ""
        qry['where'] += " facturascli.codagente = '" + str(model.i_facturascli_codagente) + "'" if qry['where'] == "" else " AND facturascli.codagente = '" + str(model.i_facturascli_codagente) + "'" if model.i_facturascli_codagente else ""
        qry['where'] += " facturascli.fecha >= '" + str(model.d_facturascli_fecha) + "'" if qry['where'] == "" else " AND facturascli.fecha >= '" + str(model.d_facturascli_fecha) + "'" if model.d_facturascli_fecha else ""
        qry['where'] += " facturascli.fecha <= '" + str(model.h_facturascli_fecha) + "'" if qry['where'] == "" else " AND facturascli.fecha <= '" + str(model.h_facturascli_fecha) + "'" if model.h_facturascli_fecha else ""
        # qry.where += datosReg.hasOwnProperty("id") ? (qry.where == "" ? "" : " AND") + " i_sh_consumocliente.id = " + datosReg.id : "";
        # qry.where += datosReg.hasOwnProperty("i_facturascli_codcliente") && datosReg.i_facturascli_codcliente != null ? (qry.where == "" ? "" : " AND") + " facturascli.codcliente = '" + datosReg.i_facturascli_codcliente + "'" : "";
        # qry.where += datosReg.hasOwnProperty("i_facturascli_codagente") && datosReg.i_facturascli_codagente != null ? (qry.where == "" ? "" : " AND") + " facturascli.codagente = '" + datosReg.i_facturascli_codagente + "'" : "";
        # qry.where += datosReg.hasOwnProperty("d_facturascli_fecha") && datosReg.d_facturascli_fecha != null ? (qry.where == "" ? "" : " AND") + " facturascli.fecha >= '" + datosReg.d_facturascli_fecha + "'" : "";
        # qry.where += datosReg.hasOwnProperty("h_facturascli_fecha") && datosReg.h_facturascli_fecha != null ? (qry.where == "" ? "" : " AND") + " facturascli.fecha <= '" + datosReg.h_facturascli_fecha + "'" : "";
        qry['group'] = ""
        qry['order'] = " ORDER BY facturascli.fecha ASC"

        print(qry)
        q = qsatype.FLSqlQuery()
        q.setTablesList("empresa, i_sh_consumocliente, agentes, facturascli, clientes")
        q.setSelect(qry['select'])
        q.setFrom(qry['from'])
        q.setWhere(qry['where'] + qry['group'] + qry['order'])
        if not q.exec_():
            print("algo fallo")
            return False
        print("size: ", q.size())

        report = {}
        report['cabeceras'] = ["Código", "Nombre", "Dirección", "CIF/NIF", "Agente", "Desde", "Hasta"]
        report['columnas'] = ["codcliente", "nombrecliente", "direccion", "cifnif", "nombreap", "d_facturascli_fecha", "h_facturascli_fecha"]
        report['tipos'] = ["string", "string", "address", "string", "string", "date", "date"]
        report['level0'] = {}
        report['level0']['cabeceras'] = ["Fecha", "Factura", "Ref.", "Descripción", "Cant.", "PVP Unit.", "PVP Total"]
        report['level0']['columnas'] = ["fecha", "codigo", "referencia", "descripcion", "cantidad", "pvpunitario", "pvptotal"]
        report['level0']['tipos'] = ["date", "string", "string", "string", "double", "currency", "currency"]
        report['level0']['totales'] = ["cantidad", "pvptotal"]
        report['level0']['colTotales'] = ["", "", "", "", "cantidad", "", "pvptotal"]
        report['level0']['tipTotales'] = ["", "", "", "", "double", "", "currency"]
        report['level0']['opTotales'] = ["", "", "", "", "suma", "", "suma"]
        return report

    def sanhigia_dameInformeConsumocliente(self, model):
        url = '/informes/i_sh_consumocliente/' + str(model.id) + '/consumocliente'
        return url

    def __init__(self, context=None):
        super(sanhigia_informes, self).__init__(context)

    def sanhigia_field_nombreagente(self, model):
        try:
            codagente = model.i_facturascli_codagente.codagente
        except Exception:
            return ""
        nombreap = qsatype.FLUtil.sqlSelect(u"agentes", u"nombreap", ustr(u"codagente = '", codagente, "'"))
        return nombreap

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

    def dameInformeConsumocliente(self, model):
        return self.ctx.sanhigia_dameInformeConsumocliente(model)

    def report_consumocliente(self, model):
        return self.ctx.sanhigia_report_consumocliente(model)


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
