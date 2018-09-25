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
                return [{'criterio': 'i_pedidoscli_codagente__in', 'valor': [agente[0].codagente]}]
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
            codagente = model.i_pedidoscli_codagente.codagente
        except Exception:
            return ""
        nombreap = qsatype.FLUtil.sqlSelect(u"agentes", u"nombreap", ustr(u"codagente = '", codagente, "'"))
        return nombreap

    def sanhigia_informes_getDesc(self):
        desc = None
        return desc

    def sanhigia_report_pedidoscli(self, model, cursor):
        qry = {}
        qry['select'] = " pedidoscli.codigo, pedidoscli.fecha, pedidoscli.codcliente, pedidoscli.nombrecliente, pedidoscli.cifnif, pedidoscli.servido, pedidoscli.neto, pedidoscli.totaliva, pedidoscli.totalrecargo, pedidoscli.total, pedidoscli.coddivisa, pedidoscli.idpedido, pedidoscli.codejercicio, agentes.nombre,"
        qry['select'] += " i_pedidoscli.d_pedidoscli_codigo," if model.d_pedidoscli_codigo else ""
        qry['select'] += " i_pedidoscli.h_pedidoscli_codigo," if model.h_pedidoscli_codigo else ""
        qry['select'] += " i_pedidoscli.d_pedidoscli_fecha," if model.d_pedidoscli_fecha else ""
        qry['select'] += " i_pedidoscli.h_pedidoscli_fecha," if model.h_pedidoscli_fecha else ""
        qry['select'] += " i_pedidoscli_servido," if model.i_pedidoscli_servido else ""
        qry['select'] += " i_pedidoscli_codcliente," if model.i_pedidoscli_codcliente else ""
        qry['select'] += " lineaspedidoscli.referencia, lineaspedidoscli.descripcion, lineaspedidoscli.cantidad, lineaspedidoscli.pvpunitario, lineaspedidoscli.pvptotal, lineaspedidoscli.codimpuesto, lineaspedidoscli.cerrada, lineaspedidoscli.iva, lineaspedidoscli.dtopor, lineaspedidoscli.totalenalbaran AS canservida, (lineaspedidoscli.cantidad - lineaspedidoscli.totalenalbaran) AS canpendiente, stocks.cantidad AS canstock," if model.lineas else ""
        qry['select'] = qry['select'][:-1]

        qry['from'] = " i_pedidoscli LEFT OUTER JOIN agentes ON i_pedidoscli.i_pedidoscli_codagente = agentes.codagente, pedidoscli"
        if model.lineas:
            qry['from'] += " INNER JOIN lineaspedidoscli ON pedidoscli.idpedido = lineaspedidoscli.idpedido INNER JOIN stocks ON (pedidoscli.codalmacen = stocks.codalmacen AND lineaspedidoscli.referencia = stocks.referencia)" if model.lineas else ""

        qry['where'] = ""
        qry['where'] += " i_pedidoscli.id = " + str(model.id) if qry['where'] == "" else " AND i_pedidoscli.id = " + str(model.id) if model.id else ""
        qry['where'] += " pedidoscli.codigo >= '" + str(model.d_pedidoscli_codigo) + "'" if qry['where'] == "" else " AND pedidoscli.codigo >= '" + str(model.d_pedidoscli_codigo) + "'" if model.d_pedidoscli_codigo else ""
        qry['where'] += " pedidoscli.codigo <= '" + str(model.h_pedidoscli_codigo) + "'" if qry['where'] == "" else " AND pedidoscli.codigo <= '" + str(model.h_pedidoscli_codigo) + "'" if model.h_pedidoscli_codigo else ""
        qry['where'] += " pedidoscli.codejercicio = '" + str(model.i_pedidoscli_codejercicio) + "'" if qry['where'] == "" else " AND pedidoscli.codejercicio = '" + str(model.i_pedidoscli_codejercicio) + "'" if model.i_pedidoscli_codejercicio else ""
        qry['where'] += " pedidoscli.fecha >= '" + str(model.d_pedidoscli_fecha) + "'" if qry['where'] == "" else " AND pedidoscli.fecha >= '" + str(model.d_pedidoscli_fecha) + "'" if model.d_pedidoscli_fecha else ""
        qry['where'] += " pedidoscli.fecha <= '" + str(model.h_pedidoscli_fecha) + "'" if qry['where'] == "" else " AND pedidoscli.fecha <= '" + str(model.h_pedidoscli_fecha) + "'" if model.h_pedidoscli_fecha else ""
        qry['where'] += " pedidoscli.codcliente = '" + str(model.i_pedidoscli_codcliente) + "'" if qry['where'] == "" else " AND pedidoscli.codcliente = '" + str(model.i_pedidoscli_codcliente) + "'" if model.i_pedidoscli_codcliente else ""
        qry['where'] += " pedidoscli.codagente = '" + str(model.i_pedidoscli_codagente.codagente) + "'" if qry['where'] == "" else " AND pedidoscli.codagente = '" + str(model.i_pedidoscli_codagente.codagente) + "'" if model.i_pedidoscli_codagente.codagente else ""

        if model.i_pedidoscli_servido and model.i_pedidoscli_servido:
            if model.i_pedidoscli_servido == "Pendiente":
                qry['where'] += "" if qry['where'] == "" else " AND"
                qry['where'] += " pedidoscli.servido IN ('No', 'Parcial')"
            elif model.i_pedidoscli_servido != "Todos":
                qry['where'] += "" if qry['where'] == "" else " AND"
                qry['where'] += " pedidoscli.servido = '" + model.i_pedidoscli_servido + "'"

        if model.solopdtes and model.solopdtes == "t":
            qry['where'] += " AND lineaspedidoscli.cerrada IS FALSE AND lineaspedidoscli.totalenalbaran < lineaspedidoscli.cantidad"

        if model.solodisponibles and model.solodisponibles == "t":
            qry['where'] += " AND lineaspedidoscli.cantidad <= stocks.cantidad"

        qry['order'] = ""
        if model.orden1:
            if model.orden1 != "No ordenar":
                qry['order'] += "" if qry['order'] == "" else " AND"
                if model.orden1 == "Código":
                    qry['order'] += ", pedidoscli.codigo"
                elif model.orden1 == "Cod.Cliente":
                    qry['order'] += ", pedidoscli.codcliente"
                elif model.orden1 == "Cliente":
                    qry['order'] += ", pedidoscli.nombrecliente"
                elif model.orden1 == "Fecha":
                    qry['order'] += ", pedidoscli.fecha"
                elif model.orden1 == "Total":
                    qry['order'] += ", pedidoscli.total"

                if model.tipoorden1:
                    qry['order'] += "ASC" if model.tipoorden1 == "Ascendente" else " DESC"

        if model.orden2:
            if model.orden2 != "No ordenar":
                qry['order'] += "" if qry['order'] == "" else " AND"
                if model.orden2 == "Código":
                    qry['order'] += ", pedidoscli.codigo"
                elif model.orden2 == "Cod.Cliente":
                    qry['order'] += ", pedidoscli.codcliente"
                elif model.orden2 == "Cliente":
                    qry['order'] += ", pedidoscli.nombrecliente"
                elif model.orden2 == "Fecha":
                    qry['order'] += ", pedidoscli.fecha"
                elif model.orden2 == "Total":
                    qry['order'] += ", pedidoscli.total"

                if model.tipoorden2:
                    qry['order'] += "ASC" if model.tipoorden2 == "Ascendente" else " DESC"

        if qry['order'] == "":
            qry['order'] = " ORDER BY pedidoscli.codigo"
        else:
            qry['order'] = " ORDER BY " + qry['order']

        qry['group'] = ""

        print(qry)
        q = qsatype.FLSqlQuery()
        q.setTablesList("i_pedidoscli, agentes, pedidoscli, lineaspedidoscli, stocks")
        q.setSelect(qry['select'])
        q.setFrom(qry['from'])
        q.setWhere(qry['where'] + qry['group'] + qry['order'])
        if not q.exec_():
            return False
        while q.next():
            print(q.value("pedidoscli.codigo"))
            print(q.value("pedidoscli.canstock"))
            print("________________________")
            # for ind in q.getQueryHeaders():
            #     print(ind)
            #     print({ind: q.value(ind)})
        print("size: ", q.size())
        report = {}
        report['cabeceras'] = ["Agente", "Desde código", "Hasta código", "Desde fecha", "Hasta fecha", "Ejercicio", "Cliente", "Servido"]
        report['columnas'] = ["nombreap", "d_pedidoscli_codigo", "h_pedidoscli_codigo", "d_pedidoscli_fecha", "h_pedidoscli_fecha", "codejercicio", "i_pedidoscli_codcliente", "i_pedidoscli_servido"]
        report['tipos'] = ["string", "string", "string", "date", "date", "string", "string", "string"]
        report['level0'] = {}
        report['level0']['cabeceras'] = ["Código", "Fecha", "Cliente", "", "", "Total"]
        report['level0']['columnas'] = ["codigo", "fecha", "nombrecliente", "", "", "total"]
        report['level0']['tipos'] = ["string", "date", "string", "", "", "currency"]
        report['level0']['colTotales'] = ["", "", "", "", "", "total"]
        report['level0']['tipTotales'] = ["", "", "", "", "", "currency"]
        report['level0']['opTotales'] = ["", "", "", "", "", "suma"]
        report['level0']['ruptura'] = ["codigo"]

        report['level1'] = {}
        report['level1']['cabeceras'] = ["Ref.", "Descripción", "Cant.", "Serv.", "Pte.", "En stock"]
        report['level1']['columnas'] = ["referencia", "descripcion", "cantidad", "canservida", "canpendiente", "canstock"]
        report['level1']['tipos'] = ["string", "string", "double", "double", "double", "double"]
        report['level1']['colTotales'] = ["", "", "cantidad", "canservida", "canpendiente", "canstock"]
        report['level1']['tipTotales'] = ["", "", "double", "double", "double", "double"]
        report['level1']['opTotales'] = ["", "", "suma", "suma", "suma", "suma"]
        return report

    def sanhigia_dameInformePedidoscli(self, model):
        url = '/informes/i_pedidoscli/' + str(model.id) + '/pedidoscli'
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

    def report_pedidoscli(self, model, cursor):
        return self.ctx.sanhigia_report_pedidoscli(model, cursor)

    def dameInformePedidoscli(self, model):
        return self.ctx.sanhigia_dameInformePedidoscli(model)


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
