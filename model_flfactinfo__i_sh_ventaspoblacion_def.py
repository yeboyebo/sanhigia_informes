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

    def sanhigia_field_nombreagente(self, model):
        try:
            codagente = model.i_facturascli_codagente.codagente
        except Exception:
            return ""
        nombreap = qsatype.FLUtil.sqlSelect(u"agentes", u"nombreap", ustr(u"codagente = '", codagente, "'"))
        return nombreap

    def sanhigia_informes_getDesc(self):
        desc = None
        return desc

    def sanhigia_report_ventaspoblacion(self, model):
        qry = {}
        qry['select'] = " empresa.nombre, empresa.cifnif, empresa.direccion, empresa.codpostal, empresa.ciudad, empresa.provincia, empresa.dirtipovia, empresa.dirnum, empresa.dirotros,"
        qry['select'] += " facturascli.codcliente, facturascli.nombrecliente, facturascli.direccion, facturascli.codpostal, UPPER(facturascli.ciudad) AS ciudadcliente, facturascli.provincia, facturascli.dirtipovia, facturascli.dirnum, facturascli.dirotros, dirclientes.telefono, i_sh_ventaspoblacion.d_facturascli_fecha, i_sh_ventaspoblacion.h_facturascli_fecha, i_sh_ventaspoblacion.i_facturascli_codagente, agentes.nombreap, SUM(facturascli.total) AS totalfacturas"
        qry['from'] = " empresa, i_sh_ventaspoblacion LEFT JOIN agentes ON i_sh_ventaspoblacion.i_facturascli_codagente = agentes.codagente, facturascli LEFT OUTER JOIN dirclientes ON facturascli.coddir = dirclientes.id"
        qry['where'] = ""
        qry['where'] += " i_sh_ventaspoblacion.id = " + str(model.id) if qry['where'] == "" else " AND i_sh_ventaspoblacion.id = " + str(model.id) if model.id else ""
        qry['where'] += " facturascli.codagente = '" + str(model.i_facturascli_codagente) + "'" if qry['where'] == "" else " AND facturascli.codagente = '" + str(model.i_facturascli_codagente) + "'" if model.i_facturascli_codagente else ""
        qry['where'] += " facturascli.fecha >= '" + str(model.d_facturascli_fecha) + "'" if qry['where'] == "" else " AND facturascli.fecha >= '" + str(model.d_facturascli_fecha) + "'" if model.d_facturascli_fecha else ""
        qry['where'] += " facturascli.fecha <= '" + str(model.h_facturascli_fecha) + "'" if qry['where'] == "" else " AND facturascli.fecha <= '" + str(model.h_facturascli_fecha) + "'" if model.h_facturascli_fecha else ""

        qry['group'] = " GROUP BY empresa.nombre, empresa.cifnif, empresa.direccion, empresa.codpostal, empresa.ciudad, empresa.provincia, empresa.dirtipovia, empresa.dirnum, empresa.dirotros, facturascli.codcliente, facturascli.nombrecliente, facturascli.direccion, facturascli.codpostal, UPPER(facturascli.ciudad), facturascli.provincia, facturascli.dirtipovia, facturascli.dirnum, facturascli.dirotros, dirclientes.telefono,"
        qry['group'] += " i_sh_ventaspoblacion.d_facturascli_fecha," if model.d_facturascli_fecha else ""
        qry['group'] += " i_sh_ventaspoblacion.h_facturascli_fecha," if model.h_facturascli_fecha else ""
        qry['group'] += " i_sh_ventaspoblacion.i_facturascli_codagente," if model.i_facturascli_codagente else ""
        qry['group'] += " agentes.nombreap," if model.i_facturascli_codagente else ""
        qry['group'] = qry['group'][:-1]

        qry['order'] = " ORDER BY UPPER(facturascli.ciudad), facturascli.codpostal, facturascli.nombrecliente"
        print(qry)
        q = qsatype.FLSqlQuery()
        q.setTablesList("empresa, i_sh_ventaspoblacion, agentes, facturascli, dirclientes")
        q.setSelect(qry['select'])
        q.setFrom(qry['from'])
        q.setWhere(qry['where'] + qry['group'] + qry['order'])
        if not q.exec_():
            print("algo fallo")
            return False
        print("size: ", q.size())

        # qry.where += datosReg.hasOwnProperty("id") ? (qry.where == "" ? "" : " AND") + " i_sh_ventaspoblacion.id = " + datosReg.id : "";
        # qry.where += datosReg.hasOwnProperty("i_facturascli_codagente") && datosReg.i_facturascli_codagente != null ? (qry.where == "" ? "" : " AND") + " facturascli.codagente = '" + datosReg.i_facturascli_codagente + "'" : "";
        # qry.where += datosReg.hasOwnProperty("d_facturascli_fecha") && datosReg.d_facturascli_fecha != null ? (qry.where == "" ? "" : " AND") + " facturascli.fecha >= '" + datosReg.d_facturascli_fecha + "'" : "";
        # qry.where += datosReg.hasOwnProperty("h_facturascli_fecha") && datosReg.h_facturascli_fecha != null ? (qry.where == "" ? "" : " AND") + " facturascli.fecha <= '" + datosReg.h_facturascli_fecha + "'" : "";

        # qry.group += datosReg.hasOwnProperty("d_facturascli_fecha") && datosReg.d_facturascli_fecha != null ? ", i_sh_ventaspoblacion.d_facturascli_fecha" : "";
        # qry.group += datosReg.hasOwnProperty("h_facturascli_fecha") && datosReg.h_facturascli_fecha != null ? ", i_sh_ventaspoblacion.h_facturascli_fecha" : "";
        # qry.group += datosReg.hasOwnProperty("i_facturascli_codagente") && datosReg.i_facturascli_codagente != null ? ", i_sh_ventaspoblacion.i_facturascli_codagente" : "";
        # qry.group += datosReg.hasOwnProperty("i_facturascli_codagente") && datosReg.i_facturascli_codagente != null ? ", agentes.nombreap" : "";
        report = {}
        report['cabeceras'] = ["Agente", "Desde", "Hasta"]
        report['columnas'] = ["nombreap", "d_facturascli_fecha", "h_facturascli_fecha"]
        report['tipos'] = ["string", "date", "date"]

        report['level0'] = {}
        report['level0']['columnas'] = ["ciudadcliente", "", "", ""]
        report['level0']['tipos'] = ["string", "", "", ""]
        report['level0']['colTotales'] = ["", "", "", "totalfacturas"]
        report['level0']['tipTotales'] = ["", "", "", "currency"]
        report['level0']['opTotales'] = ["", "", "", "suma"]
        report['level0']['ruptura'] = ["ciudadcliente"]

        report['level1'] = {}
        report['level1']['columnas'] = ["codpostal", "", "", ""]
        report['level1']['tipos'] = ["string", "", "", ""]
        report['level1']['colTotales'] = ["", "", "", "totalfacturas"]
        report['level1']['tipTotales'] = ["", "", "", "currency"]
        report['level1']['opTotales'] = ["", "", "", "suma"]
        report['level1']['ruptura'] = ["codpostal"]

        report['level2'] = {}
        report['level2']['cabeceras'] = ["Cliente", "Dirección", "Teléfono", "Total"]
        report['level2']['columnas'] = ["nombrecliente", "direccion", "telefono", "totalfacturas"]
        report['level2']['tipos'] = ["string", "address2", "string", "currency"]
        report['level2']['colTotales'] = ["", "", "", "totalfacturas"]
        report['level2']['tipTotales'] = ["", "", "", "currency"]
        report['level2']['opTotales'] = ["", "", "", "suma"]
        return report

    def sanhigia_dameInformeVentaspoblacion(self, model):
        url = '/informes/i_sh_ventaspoblacion/' + str(model.id) + '/ventaspoblacion'
        return url

    def __init__(self, context=None):
        super().__init__(context)

    def field_nombreagente(self, model):
        return self.ctx.sanhigia_field_nombreagente(model)

    def getFilters(self, model, name, template=None):
        return self.ctx.sanhigia_informes_getFilters(model, name, template)

    def getForeignFields(self, model, template=None):
        return self.ctx.sanhigia_informes_getForeignFields(model, template)

    def getDesc(self):
        return self.ctx.sanhigia_informes_getDesc()

    def report_ventaspoblacion(self, model):
        return self.ctx.sanhigia_report_ventaspoblacion(model)

    def dameInformeVentaspoblacion(self, model):
        return self.ctx.sanhigia_dameInformeVentaspoblacion(model)


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
