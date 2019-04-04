# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *
from models.flfactppal.agentes import agentes
from models.flfactinfo import flfactinfo_def


class sanhigia_informes(interna):

    def sanhigia_informes_getFilters(self, model, name, template=None):
        filters = []
        if name == 'filtroagente':
            usuario = qsatype.FLUtil.nameUser()
            codGrupo = qsatype.FLUtil.sqlSelect(u"flusers", u"idgroup", ustr(u"iduser = '", usuario, u"' AND idgroup = 'Administracion'"))
            if codGrupo:
                return filters
            else:
                codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
                if not codagente:
                    codagente = '-1'
                return [{'criterio': 'i_clientes_codagente__exact', 'valor': codagente}]
        print("Filters: ", filters)
        return filters

    def sanhigia_informes_getForeignFields(self, model, template=None):
        fields = []
        if template == 'master':
            return [
                {'verbose_name': 'nombreagente', 'func': 'field_nombreagente'},
                {'verbose_name': 'nombrearticulo', 'func': 'field_nombrearticulo'}
            ]
        return fields

    def sanhigia_informes_field_nombreagente(self, model):
        try:
            return model.i_clientes_codagente.nombreap
        except Exception:
            return ""

    def sanhigia_informes_field_nombrearticulo(self, model):
        print("model.referencias.descripcion")
        try:
            return model.referencias.descripcion
        except Exception:
            return ""

    def sanhigia_informes_getDesc(self):
        desc = None
        return desc

    def sanhigia_informes_iniciaValoresCursor(self, cursor=None):
        usuario = qsatype.FLUtil.nameUser()
        print("usuario: ", usuario)
        codGrupo = qsatype.FLUtil.sqlSelect(u"flusers", u"idgroup", ustr(u"iduser = '", usuario, u"' AND idgroup = 'Administracion'"))
        if codGrupo:
            codagente = ''
        else:
            codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
            if not codagente:
                codagente = ''
        print("codagente: ", codagente)
        cursor.setValueBuffer(u"i_clientes_codagente", codagente)
        return True

    def sanhigia_informes_checkCodAgente(self, cursor):
        if not flfactinfo_def.iface.esadmin(qsatype.FLUtil.nameUser()):
            return "disabled"
        return True

    def sanhigia_informes_generarReport(self, model):
        _i = self.iface
        report = {}
        oParam = {}
        oParam = _i.dameParamInforme(model)
        report['reportName'] = "i_clientesventaart"
        report['params'] = {}
        formato = "%d-%m-%Y"
        if model.i_clientes_codagente and model.i_clientes_codagente.nombreap != "":
            report['params']['nombreagente'] = model.i_clientes_codagente.nombreap
        if model.fechadesde and model.fechadesde != "":
            fechadesde = model.fechadesde.strftime(formato)
            report['params']['fechadesde'] = fechadesde
        if model.fechahasta and model.fechahasta != "":
            fechahasta = model.fechahasta.strftime(formato)
            report['params']['fechahasta'] = fechahasta
        report['params']['WHERE'] = oParam['where']
        report['disposition'] = "inline"
        return report

    def sanhigia_informes_dameParamInforme(self, model):
        oParamInforme = {}
        oParamInforme['where'] = ""
        if model.i_clientes_codagente and model.i_clientes_codagente.codagente != "":
            if oParamInforme['where'] != "":
                oParamInforme['where'] += " AND "
            oParamInforme['where'] += "facturascli.codagente = '" + str(model.i_clientes_codagente.codagente) + "'"
        if model.fechadesde and model.fechadesde != "":
            if oParamInforme['where'] != "":
                oParamInforme['where'] += " AND "
            oParamInforme['where'] += "facturascli.fecha >= '" + str(model.fechadesde) + "'"
        if model.fechahasta and model.fechahasta != "":
            if oParamInforme['where'] != "":
                oParamInforme['where'] += " AND "
            oParamInforme['where'] += "facturascli.fecha <= '" + str(model.fechahasta) + "'"
        if model.referencias and model.referencias.referencia != "":
            if oParamInforme['where'] != "":
                oParamInforme['where'] += " AND "
            oParamInforme['where'] += "lineasfacturascli.referencia IN ('" + str(model.referencias.referencia) + "')"
        return oParamInforme

    def __init__(self, context=None):
        super().__init__(context)

    def field_nombreagente(self, model):
        return self.ctx.sanhigia_informes_field_nombreagente(model)

    def field_nombrearticulo(self, model):
        return self.ctx.sanhigia_informes_field_nombrearticulo(model)

    def getFilters(self, model, name, template=None):
        return self.ctx.sanhigia_informes_getFilters(model, name, template)

    def getForeignFields(self, model, template=None):
        return self.ctx.sanhigia_informes_getForeignFields(model, template)

    def getDesc(self):
        return self.ctx.sanhigia_informes_getDesc()

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.sanhigia_informes_iniciaValoresCursor(cursor)

    def checkCodAgente(self, cursor):
        return self.ctx.sanhigia_informes_checkCodAgente(cursor)

    def generarReport(self, model):
        return self.ctx.sanhigia_informes_generarReport(model)

    def dameParamInforme(self, model):
        return self.ctx.sanhigia_informes_dameParamInforme(model)


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
