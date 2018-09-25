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
            # print(usr, usr != "infosial", usr != "infosial" and usr != "jesus")
            if usr != "infosial" and usr != "jesus":
                try:
                    agente = agentes.objects.filter(idusuario__exact=usr)
                except Exception as e:
                    print(e)
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
            codagente = model.codagente.codagente
        except Exception:
            return ""
        nombreap = qsatype.FLUtil.sqlSelect(u"agentes", u"nombreap", ustr(u"codagente = '", codagente, "'"))
        return nombreap

    def sanhigia_checkCodAgente(self, cursor):
        grupo = qsatype.FLUtil.sqlSelect(u"flusers", u"idgroup", ustr(u"iduser = '", qsatype.FLUtil.nameUser(), u"'"))
        if grupo != "Administracion":
            return "disabled"
        return True

    def sanhigia_informes_getDesc(self):
        desc = None
        return desc

    def sanhigia_report_ventasarticulo(self, model):
        qry = {}
        qry['select'] = "lf.referencia, a.descripcion, case SUM(lf.cantidad * a.pvp) when 0 then 0 else ((SUM(lf.cantidad * a.pvp) - SUM(lf.pvptotal)) * 100 / SUM(lf.cantidad * a.pvp)) end AS dto, SUM(lf.pvptotal) AS total, "
        qry['select'] += " va.fechadesde," if model.fechadesde else ""
        qry['select'] += " va.fechahasta," if model.fechahasta else ""
        qry['select'] += " agentes.nombreap," if model.codagente else ""
        qry['select'] += " f.codserie," if model.codserie else ""
        qry['select'] += " a.codfamilia," if model.codfamilia else ""
        qry['select'] += " a.codsubfamilia," if model.codsubfamilia else ""
        qry['select'] = qry['select'][:-1]

        qry['from'] = " facturascli f INNER JOIN lineasfacturascli lf ON f.idfactura = lf.idfactura INNER JOIN articulos a ON lf.referencia = a.referencia  LEFT OUTER JOIN series s ON f.codserie = s.codserie, i_sh_ventasarticulo va LEFT OUTER JOIN agentes ON va.codagente = agentes.codagente"

        qry['where'] = ""
        qry['where'] += " va.id = " + str(model.id) if qry['where'] == "" else " AND va.id = " + str(model.id) if model.id else ""
        qry['where'] += " f.codagente = '" + str(model.codagente) + "'" if qry['where'] == "" else " AND f.codagente = '" + str(model.codagente) + "'" if model.codagente else ""
        qry['where'] += " f.fecha >= '" + str(model.fechadesde) + "'" if qry['where'] == "" else " AND f.fecha >= '" + str(model.fechadesde) + "'" if model.fechadesde else ""
        qry['where'] += " f.fecha <= '" + str(model.fechahasta) + "'" if qry['where'] == "" else " AND f.fecha <= '" + str(model.fechahasta) + "'" if model.fechahasta else ""
        qry['where'] += " f.codserie = '" + str(model.codserie) + "'" if qry['where'] == "" else " AND f.codserie = '" + str(model.codserie) + "'" if model.codserie else ""
        qry['where'] += " a.codfamilia = '" + str(model.codfamilia) + "'" if qry['where'] == "" else " AND a.codfamilia = '" + str(model.codfamilia) + "'" if model.codfamilia else ""
        qry['where'] += " a.codsubfamilia = '" + str(model.codsubfamilia) + "'" if qry['where'] == "" else " AND a.codsubfamilia = '" + str(model.codsubfamilia) + "'" if model.codsubfamilia else ""

        qry['order'] = " ORDER BY SUM(lf.pvptotal) DESC"

        qry['group'] = " GROUP BY lf.referencia, a.descripcion,"

        qry['group'] += " va.fechadesde," if model.fechadesde else ""
        qry['group'] += " va.fechahasta," if model.fechahasta else ""
        qry['group'] += " agentes.nombreap," if model.codagente else ""
        qry['group'] += " f.codserie," if model.codserie else ""
        qry['group'] += " a.codfamilia," if model.codfamilia else ""
        qry['group'] += " a.codsubfamilia," if model.codsubfamilia else ""

        qry['group'] = qry['group'][:-1]
        print(qry)
        q = qsatype.FLSqlQuery()
        q.setTablesList("facturascli, lineasfacturascli, articulos, series, i_sh_ventasarticulo")
        q.setSelect(qry['select'])
        q.setFrom(qry['from'])
        q.setWhere(qry['where'] + qry['group'] + qry['order'])
        if not q.exec_():
            print("algo fallo")
            return False
        print("size: ", q.size())

        report = {}
        report['cabeceras'] = ["Agente", "Desde", "Hasta", "Serie", "Familia", "Subfamilia"]
        report['columnas'] = ["nombreap", "fechadesde", "fechahasta", "codserie", "codfamilia", "codsubfamilia"]
        report['tipos'] = ["string", "date", "date", "string", "string", "string"]
        report['level0'] = {}
        report['level0']['cabeceras'] = ["Referencia", "Artículo", "Dto.", "Total"]
        report['level0']['columnas'] = ["referencia", "descripcion", "dto", "total"]
        report['level0']['tipos'] = ["string", "string", "percentage", "currency"]
        report['level0']['colTotales'] = ["", "", "dto", "total"]
        report['level0']['tipTotales'] = ["", "", "percentage", "currency"]
        report['level0']['opTotales'] = ["", "", "funcion", "suma"]

        return report

    def sanhigia_dameInformeVentasarticulo(self, model):
        url = '/informes/i_sh_ventasarticulo/' + str(model.id) + '/ventasarticulo'
        return url

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

    def checkCodAgente(self, cursor):
        return self.ctx.sanhigia_checkCodAgente(cursor)

    def report_ventasarticulo(self, model):
        return self.ctx.sanhigia_report_ventasarticulo(model)

    def dameInformeVentasarticulo(self, model):
        return self.ctx.sanhigia_dameInformeVentasarticulo(model)


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
