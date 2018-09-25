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
                return [{'criterio': 'codagente__in', 'valor': [agente[0].codagente]}]
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
            codagente = cursor.valueBuffer("codagente").codagente
        except Exception:
            return ""
        nombreap = qsatype.FLUtil.sqlSelect(u"agentes", u"nombreap", ustr(u"codagente = '", codagente, "'"))
        return nombreap

    def sanhigia_informes_getDesc(self):
        desc = None
        return desc

    def sanhigia_report_ventasfamilia(self, model, cursor):
        print(cursor.valueBuffer("codagente"))
        print(" agentes.nombreap," if cursor.valueBuffer("codagente") else "")
        qry = {}
        qry['select'] = " a.codfamilia, fa.descripcion AS famdesc, a.codsubfamilia, s.descripcion AS subfamdesc, case SUM(lf.cantidad * a.pvp) when 0 then 0 else ((SUM(lf.cantidad * a.pvp) - SUM(lf.pvptotal)) * 100 / SUM(lf.cantidad * a.pvp)) end AS dto, SUM(lf.pvptotal) AS total, "
        qry['select'] += " vf.fechadesde," if model.fechadesde else ""
        qry['select'] += " vf.fechahasta," if model.fechahasta else ""
        qry['select'] += " agentes.nombreap," if cursor.valueBuffer("codagente") else ""
        qry['select'] += " f.codserie," if model.codserie else ""
        qry['select'] = qry['select'][:-1]

        qry['from'] = " facturascli f INNER JOIN lineasfacturascli lf ON f.idfactura = lf.idfactura INNER JOIN articulos a ON lf.referencia = a.referencia INNER JOIN familias fa ON a.codfamilia = fa.codfamilia INNER JOIN subfamilias s ON a.codsubfamilia = s.codsubfamilia LEFT OUTER JOIN series se ON f.codserie = se.codserie, i_sh_ventasfamilia vf LEFT OUTER JOIN agentes ON vf.codagente = agentes.codagente"

        qry['where'] = ""
        qry['where'] += " vf.id = " + str(model.id) if qry['where'] == "" else " AND vf.id = " + str(model.id) if model.id else ""
        qry['where'] += " f.codagente = '" + str(cursor.valueBuffer("codagente")) + "'" if qry['where'] == "" else " AND f.codagente = '" + str(cursor.valueBuffer("codagente")) + "'" if cursor.valueBuffer("codagente") else ""
        qry['where'] += " f.fecha >= '" + str(model.fechadesde) + "'" if qry['where'] == "" else " AND f.fecha >= '" + str(model.fechadesde) + "'" if model.fechadesde else ""
        qry['where'] += " f.fecha <= '" + str(model.fechahasta) + "'" if qry['where'] == "" else " AND f.fecha <= '" + str(model.fechahasta) + "'" if model.fechahasta else ""
        qry['where'] += " f.codserie = '" + str(model.codserie) + "'" if qry['where'] == "" else " AND f.codserie = '" + str(model.codserie) + "'" if model.codserie else ""

        qry['order'] = " ORDER BY a.codfamilia, a.codsubfamilia, SUM(lf.pvptotal) DESC"

        qry['group'] = " GROUP BY a.codfamilia, a.codsubfamilia, fa.descripcion, s.descripcion, "
        qry['group'] += " vf.fechadesde," if model.fechadesde else ""
        qry['group'] += " vf.fechahasta," if model.fechahasta else ""
        qry['group'] += " agentes.nombreap," if cursor.valueBuffer("codagente") else ""
        qry['group'] += " f.codserie," if model.codserie else ""
        qry['group'] = qry['group'][:-1]

        print(qry)
        q = qsatype.FLSqlQuery()
        q.setTablesList("facturascli, lineasfacturascli, articulos, series, familias, subfamilias, i_sh_ventasfamilia, agentes")
        q.setSelect(qry['select'])
        q.setFrom(qry['from'])
        q.setWhere(qry['where'] + qry['group'] + qry['order'])
        if not q.exec_():
            print("algo fallo")
            return False
        print("size: ", q.size())

        report = {}
        report['cabeceras'] = ["Agente", "Desde", "Hasta", "Serie"]
        report['columnas'] = ["nombreap", "fechadesde", "fechahasta", "codserie"]
        report['tipos'] = ["string", "date", "date", "string"]
        report['level0'] = {}
        report['level0']['cabeceras'] = ["Código", "Familia", "", ""]
        report['level0']['columnas'] = ["codfamilia", "famdesc", "", ""]
        report['level0']['tipos'] = ["string", "string", "", ""]
        report['level0']['colTotales'] = ["", "", "dto", "total"]
        report['level0']['tipTotales'] = ["", "", "percentage", "currency"]
        report['level0']['opTotales'] = ["", "", "funcion", "suma"]
        report['level0']['ruptura'] = ["codfamilia"]

        report['level1'] = {}
        report['level1']['cabeceras'] = ["Código", "Subfamilia", "Dto.", "Total"]
        report['level1']['columnas'] = ["codsubfamilia", "subfamdesc", "dto", "total"]
        report['level1']['tipos'] = ["string", "string", "percentage", "currency"]
        report['level1']['colTotales'] = ["", "", "dto", "total"]
        report['level1']['tipTotales'] = ["", "", "percentage", "currency"]
        report['level1']['opTotales'] = ["", "", "funcion", "suma"]
        report['level1']['ruptura'] = ["codsubfamilia"]
        return report

    def sanhigia_dameInformeVentasfamilia(self, model):
        # url = '/informes/i_sh_ventasfamilia/' + str(model.id) + '/ventasfamilia'
        # return url
        where = ""
        where += " facturascli.codagente = '" + str(model.codagente.codagente) + "'" if where == "" else " AND facturascli.codagente = '" + str(model.codagente.codagente) + "'" if model.codagente.codagente else ""
        where += " facturascli.fecha >= '" + str(model.fechadesde) + "'" if where == "" else " AND facturascli.fecha >= '" + str(model.fechadesde) + "'" if model.fechadesde else ""
        where += " facturascli.fecha <= '" + str(model.fechahasta) + "'" if where == "" else " AND facturascli.fecha <= '" + str(model.fechahasta) + "'" if model.fechahasta else ""
        where += " facturascli.codserie = '" + str(model.codserie) + "'" if where == "" else " AND facturascli.codserie = '" + str(model.codserie) + "'" if model.codserie else ""
        report = {}
        report['reportName'] = "jsenar/ventasfamilia"
        report['disposition'] = "inline"
        report['params'] = {}
        print("_______________________")
        print(where)
        report["params"]["WHERE"] = where
        # report['params']['WHERE'] = "(facturascli.fecha >= '2018-02-01' AND facturascli.fecha <= '2018-02-02' AND facturascli.codagente = '37' AND i_sh_ventasfamilia.id = 339 )"
        # report['params']['WHERE'] = "facturascli.codigo = '" + model.codigo + "'"
        # return True
        return report

    def __init__(self, context=None):
        super(sanhigia_informes, self).__init__(context)

    def field_nombreagente(self, model):
        return self.ctx.sanhigia_field_nombreagente(model)

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

    def report_ventasfamilia(self, model, cursor):
        return self.ctx.sanhigia_report_ventasfamilia(model, cursor)

    def dameInformeVentasfamilia(self, model):
        return self.ctx.sanhigia_dameInformeVentasfamilia(model)


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
