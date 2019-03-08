
# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *
from datetime import datetime


class sanhigia_informes(interna):

    def sanhigia_informes_funcion(self, model):
        _i = self.iface
        graficos = {}
        usuario = qsatype.FLUtil.nameUser()
        formato = "%d-%m-%Y"
        codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
        nombreagente = qsatype.FLUtil.sqlSelect(u"agentes", u"nombreap", ustr(u"codagente = '", codagente, u"'"))
        aux = datetime.now()
        fechahoy = aux.date()
        print("HOY____", fechahoy)
        q = qsatype.FLSqlQuery()
        q.setSelect(u"ROUND(CAST(objetivo AS numeric), 2),fechainicio,fechafin")
        q.setFrom(u"sh_previsiones")
        q.setWhere(ustr(u"codagente = '", codagente, u"' AND CURRENT_DATE BETWEEN fechainicio AND fechafin"))
        if not q.exec_():
            valor = 0
            texto = "No existe una previsión para la fecha {0} y el agente ( {1})".format(fechahoy.strftime(formato), nombreagente)
            graficos["g1"] = {"value": valor, "mainColor": None, "text": texto, "showInnerText": False}
            return graficos
        print("Consulta_____:", q.sql())
        objetivo = 0
        if q.first():
            objetivo = q.value(0)
            fechainicio = q.value(1)
            fechafin = q.value(2)
        else:
            valor = 0
            texto = "No existe una previsión para la fecha {0} y el agente ( {1})".format(fechahoy.strftime(formato), nombreagente)
            graficos["g1"] = {"value": valor, "mainColor": None, "text": texto, "showInnerText": False}
            return graficos
        dif = (fechafin - fechainicio).days
        difcurrent = (fechahoy - fechainicio).days
        where = u"codagente = '" + codagente + u"' AND f.fecha BETWEEN '" + ustr(fechainicio) + "' AND CURRENT_DATE "
        series = qsatype.FactoriaModulos.get('flfactppal').iface.pub_valorDefecto("seriesexcluidos")
        if series and series != "":
            series = series.split(",")
            where += " AND f.codserie NOT IN ('" + series.join("','") + "') "
        # where += qsatype.FactoriaModulos.get('formRecordsh_previsiones').iface.dameWhereLineasPrev()
        where += " AND m.incluirenprev = true AND f.codcliente not in (select codcliente from clientes where codgrupocompras is not null)"
        venta = qsatype.FLUtil.sqlSelect(u"lineasfacturascli lf INNER JOIN facturascli f ON lf.idfactura = f.idfactura INNER JOIN articulos a ON lf.referencia = a.referencia INNER JOIN familias m ON a.codfamilia = m.codfamilia", u"ROUND(CAST(SUM(lf.pvptotal) AS numeric), 2)", ustr(where))
        if objetivo is None or venta is None:
            valor = 0
            texto = "No existe una previsión para la fecha {0} y el agente ( {1})".format(fechahoy, nombreagente)
            graficos["g1"] = {"value": valor, "mainColor": null, "text": texto, "showInnerText": False}
            return graficos

        valor = (float(venta) / float(objetivo)) * 100
        calculo = (float(venta) / (float(objetivo) * (difcurrent / dif))) * 100
        color = _i.dameColorBarra(calculo)
        objetivo = qsatype.FLUtil.formatoMiles(objetivo)
        venta = qsatype.FLUtil.formatoMiles(venta)
        valor = round(valor, 2)
        texto = "Objetivo: {0} €.  Alcanzado: {1} € ({2} %)".format(objetivo, venta, qsatype.FLUtil.formatoMiles(valor))
        # calculo = round(calculo, 2)
        graficos["g1"] = {"value": valor, "mainColor": color, "text": texto, "showInnerText": False}
        return graficos

    def sanhigia_informes_dameColorBarra(self, calculo):
        color = ""
        if calculo < 80:
            color = "red"
        elif calculo >= 80 and calculo < 95:
            color = "orange"
        elif calculo >= 95 and calculo < 105:
            color = "lightgreen"
        else:
            color = "blue"
        return color

    def __init__(self, context=None):
        self.ctx = context

    def funcion(self, model):
        return self.ctx.sanhigia_informes_funcion(model)

    def dameColorBarra(self, calculo):
        return self.ctx.sanhigia_informes_dameColorBarra(calculo)

