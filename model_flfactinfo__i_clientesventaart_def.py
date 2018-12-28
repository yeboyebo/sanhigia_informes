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
                return [{'criterio': 'i_clientes_codagente__in', 'valor': [agente[0].codagente]}]
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
            codagente = model.i_clientes_codagente.codagente
        except Exception:
            return ""
        nombreap = qsatype.FLUtil.sqlSelect(u"agentes", u"nombreap", ustr(u"codagente = '", codagente, "'"))
        return nombreap

    def sanhigia_informes_getDesc(self):
        desc = None
        return desc

    def sanhigia_report_clientesporarticulo(self, model):
        qry = {}
        qry['select'] = " clientes.codcliente, clientes.nombre, dirclientes.dirtipovia, dirclientes.direccion, dirclientes.dirnum, dirclientes.dirotros, dirclientes.ciudad, dirclientes.codpostal, dirclientes.provincia, clientes.email, clientes.telefono1, paises.nombre AS pais, i_clientesventaart.descripcion, i_clientesventaart.fechadesde, i_clientesventaart.fechahasta, articulos.referencia, articulos.descripcion, agentes.nombreap, SUM(lineasfacturascli.cantidad) AS cantidad"
        qry['from'] = " i_clientesventaart LEFT JOIN agentes ON i_clientesventaart.i_clientes_codagente = agentes.codagente, facturascli INNER JOIN clientes ON facturascli.codcliente = clientes.codcliente INNER JOIN lineasfacturascli ON facturascli.idfactura = lineasfacturascli.idfactura INNER JOIN articulos ON lineasfacturascli.referencia = articulos.referencia LEFT OUTER JOIN dirclientes ON dirclientes.codcliente = clientes.codcliente AND dirclientes.domfacturacion INNER JOIN paises ON dirclientes.codpais = paises.codpais"

        qry['where'] = ""
        qry['where'] += " i_clientesventaart.id = " + str(model.id) if qry['where'] == "" else " AND i_clientesventaart.id = " + str(model.id) if model.id else ""
        qry['where'] += " facturascli.fecha >= '" + str(model.fechadesde) + "'" if qry['where'] == "" else " AND facturascli.fecha >= '" + str(model.fechadesde) + "'" if model.fechadesde else ""
        qry['where'] += " facturascli.fecha <= '" + str(model.fechahasta) + "'" if qry['where'] == "" else " AND facturascli.fecha <= '" + str(model.fechahasta) + "'" if model.fechahasta else ""
        qry['where'] += " clientes.codagente = '" + str(model.i_clientes_codagente) + "'" if qry['where'] == "" else " AND clientes.codagente = '" + str(model.i_clientes_codagente) + "'" if model.i_clientes_codagente else ""
        if model.referencias:
            aRef = str(model.referencias).split("\n")
            if aRef[len(aRef) - 1] == "":
                aRef.pop()
            sRef = "'" + "','".join(aRef) + "'"
            qry['where'] += "" if qry['where'] == "" else " AND"
            qry['where'] += " lineasfacturascli.referencia IN (" + sRef + ")"

        qry['group'] = " GROUP BY clientes.codcliente, clientes.nombre, dirclientes.dirtipovia, dirclientes.direccion, dirclientes.dirnum, dirclientes.dirotros, dirclientes.ciudad, dirclientes.codpostal, dirclientes.provincia, clientes.email, clientes.telefono1, paises.nombre, i_clientesventaart.descripcion, i_clientesventaart.fechadesde, i_clientesventaart.fechahasta, articulos.referencia, articulos.descripcion, agentes.nombreap"
        qry['order'] = " ORDER BY clientes.codcliente, articulos.referencia"
        print(qry)
        q = qsatype.FLSqlQuery()
        q.setTablesList("i_clientesventaart, agentes, clientes, lineasfacturascli, articulos, dirclientes, paises")
        q.setSelect(qry['select'])
        q.setFrom(qry['from'])
        q.setWhere(qry['where'] + qry['group'] + qry['order'])
        if not q.exec_():
            print("algo fallo")
            return False
        print("size: ", q.size())
        # qry.where += " lineasfacturascli.cantidad > 0";
        # qry.where += datosReg.hasOwnProperty("id") ? (qry.where == "" ? "" : " AND") + " i_clientesventaart.id = " + datosReg.id : "";
        # qry.where += datosReg.hasOwnProperty("fechadesde") && datosReg.fechadesde != null ? (qry.where == "" ? "" : " AND") + " facturascli.fecha >= '" + datosReg.fechadesde + "'" : "";
        # qry.where += datosReg.hasOwnProperty("fechahasta") && datosReg.fechahasta != null ? (qry.where == "" ? "" : " AND") + " facturascli.fecha <= '" + datosReg.fechahasta + "'" : "";
        # qry.where += datosReg.hasOwnProperty("i_clientes_codagente") && datosReg.i_clientes_codagente != null ? (qry.where == "" ? "" : " AND") + " clientes.codagente = '" + datosReg.i_clientes_codagente + "'" : "";

        # if(datosReg.hasOwnProperty("referencias") && datosReg.referencias != null) {
        #     var aRef = datosReg.referencias.split("\n");
        #     if(aRef[aRef.length - 1] == "")
        #         aRef.pop();
        #     var sRef = "'" + aRef.join("','") + "'";

        #     qry.where += qry.where == "" ? "" : " AND";
        #     qry.where += " lineasfacturascli.referencia IN (" + sRef + ")";
        # }




        report = {}
        report['cabeceras'] = ["Agente", "Desde", "Hasta"]
        report['columnas'] = ["nombreap", "fechadesde", "fechahasta"]
        report['tipos'] = ["string", "date", "date"]
        report['level0'] = {}
        report['level0']['cabeceras'] = ["Código", "Nombre", "Dirección"]
        report['level0']['columnas'] = ["codcliente", "nombre", "direccion"]
        report['level0']['tipos'] = ["string", "string", "address"]
        report['level0']['ruptura'] = ["codcliente"]

        report['level1'] = {}
        report['level1']['cabeceras'] = ["Ref.", "Descripción", "Cant."]
        report['level1']['columnas'] = ["referencia", "descripcion", "cantidad"]
        report['level1']['tipos'] = ["string", "string", "double"]
        report['level1']['colTotales'] = ["", "", "cantidad"]
        report['level1']['tipTotales'] = ["", "", "double"]
        report['level1']['opTotales'] = ["", "", "suma"]

        return report

    def sanhigia_dameInformeClientesporarticulo(self, model):
        url = '/informes/i_clientesventaart/' + str(model.id) + '/clientesporarticulo'
        return url

    def __init__(self, context=None):
        super().__init__(context)

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

    def report_clientesporarticulo(self, model):
        return self.ctx.sanhigia_report_clientesporarticulo(model)

    def dameInformeClientesporarticulo(self, model):
        return self.ctx.sanhigia_dameInformeClientesporarticulo(model)


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
