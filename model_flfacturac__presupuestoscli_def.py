
# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *
from YBUTILS.viewREST import cacheController
from YBUTILS import notifications


class sanhigia_informes(flfacturac):

    def sanhigia_informes_initValidation(self, name, data=None):
        response = True
        cacheController.setSessionVariable(ustr(u"presupuestoscli_", qsatype.FLUtil.nameUser()), data["DATA"]["idpresupuesto"])
        return response

    def sanhigia_informes_validateCursor(self, cursor):
        coddir = cursor.valueBuffer("coddir")
        if not coddir:
            qsatype.FLUtil.ponMsgError("El campo Dir. no esta informado. Por favor, selecciona un codigo valido.")
            return False
        return True

    def sanhigia_informes_getFilters(self, model, name, template=None):
        filters = []
        if name == 'presupuestosUsuario':
            # filters = [{'criterio': 'editable__exact', 'valor': True}]
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
        return None
        if model.impreso is True:
            return "cSuccess"
        else:
            return None

    def sanhigia_informes_getDesc(self):
        desc = "nombrecliente"
        return desc

    def sanhigia_informes_imprimirPresupuestoPDA(self, model):
        report = {}
        deCondiciones = qsatype.FLUtil.sqlSelect(u"presupuestoscli", u"decondiciones", ustr(u"codigo = '", model.codigo, u"'"))
        if deCondiciones is not True:
            report['reportName'] = "sh_presupuestoscli"
        else:
            report['reportName'] = "sh_presupuestosclicond"
        report['params'] = {}
        report['params']['WHERE'] = "presupuestoscli.codigo = '" + model.codigo + "'"
        return report

    def sanhigia_informes_queryGrid_histArticulosCli(self, model, filters):
        idpresupuesto = cacheController.getSessionVariable(ustr(u"presupuestoscli_", qsatype.FLUtil.nameUser()))
        query = {}
        query["tablesList"] = ("articulos,lineaspresupuestoscli,presupuestoscli")
        query["select"] = ("articulos.referencia, articulos.descripcion, MAX(presupuestoscli.fecha) as fecha")
        query["from"] = ("articulos INNER JOIN lineaspresupuestoscli ON articulos.referencia = lineaspresupuestoscli.referencia INNER JOIN presupuestoscli ON lineaspresupuestoscli.idpresupuesto = presupuestoscli.idpresupuesto")
        # query["where"] = ("presupuestoscli.codcliente = '" + model.codcliente.codcliente + "' AND lineaspresupuestoscli.idpresupuesto <> '" + ustr(idpresupuesto) + "'")
        query["where"] = "presupuestoscli.codcliente = '{0}' AND lineaspresupuestoscli.idpresupuesto <> '{1}' AND articulos.sevende".format(model.codcliente.codcliente, idpresupuesto)
        query["groupby"] = " articulos.referencia, articulos.descripcion"
        query["orderby"] = "fecha DESC"
        return query

    def sanhigia_informes_checkCondiciones(self, cursor):
        codCliente = cursor.valueBuffer(u"codcliente")
        idPresupuesto = cursor.valueBuffer(u"idpresupuesto")
        codPresCondicion = qsatype.FLUtil.sqlSelect(u"presupuestoscli", u"codigo", ustr(u"decondiciones IS TRUE AND codcliente = '", codCliente, u"' AND idpresupuesto <> ", idPresupuesto))
        if codPresCondicion:
            return "disabled"
        return True

    def __init__(self, context=None):
        super().__init__(context)

    def initValidation(self, name, data=None):
        return self.ctx.sanhigia_informes_initValidation(name, data)

    def validateCursor(self, cursor):
        return self.ctx.sanhigia_informes_validateCursor(cursor)

    def getFilters(self, model, name, template=None):
        return self.ctx.sanhigia_informes_getFilters(model, name, template)

    def getForeignFields(self, model, template=None):
        return self.ctx.sanhigia_informes_getForeignFields(model, template)

    def getDesc(self):
        return self.ctx.sanhigia_informes_getDesc()

    def imprimirPresupuestoPDA(self, model):
        return self.ctx.sanhigia_informes_imprimirPresupuestoPDA(model)

    def queryGrid_histArticulosCli(self, model, filters):
        return self.ctx.sanhigia_informes_queryGrid_histArticulosCli(model, filters)

    def field_colorRow(self, model):
        return self.ctx.sanhigia_informes_field_colorRow(model)

    def checkCondiciones(self, cursor):
        return self.ctx.sanhigia_informes_checkCondiciones(cursor)

