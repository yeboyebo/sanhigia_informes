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
            if flfactinfo_def.iface.esadmin(usuario):
                return filters
            else:
                codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
                print("codagente: ", codagente)
                if not codagente:
                    codagente = '-1'
                return [{'criterio': 'i_facturascli_codagente__exact', 'valor': codagente}]
        return filters

    def sanhigia_informes_getForeignFields(self, model, template=None):
        fields = []
        if template == 'master':
            return [
                {'verbose_name': 'nombreagente', 'func': 'field_nombreagente'}
            ]
        return fields

    def sanhigia_informes_field_nombreagente(self, model):
        try:
            return model.i_facturascli_codagente.nombreap
        except Exception:
            return ""

    def sanhigia_informes_getDesc(self):
        desc = None
        return desc

    def sanhigia_informes_iniciaValoresCursor(self, cursor=None):
        usuario = qsatype.FLUtil.nameUser()
        if flfactinfo_def.iface.esadmin(usuario):
            codagente = ''
        else:
            codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
            if not codagente:
                codagente = ''
        cursor.setValueBuffer(u"i_facturascli_codagente", codagente)
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
        report['reportName'] = "i_sh_ventaspoblacion"
        report['params'] = {}
        formato = "%d-%m-%Y"
        if model.i_facturascli_codagente and model.i_facturascli_codagente.nombreap != "":
            report['params']['nombreagente'] = model.i_facturascli_codagente.nombreap
        if model.d_facturascli_fecha and model.d_facturascli_fecha != "":
            fechadesde = model.d_facturascli_fecha.strftime(formato)
            report['params']['fechadesde'] = fechadesde
        if model.h_facturascli_fecha and model.h_facturascli_fecha != "":
            fechahasta = model.h_facturascli_fecha.strftime(formato)
            report['params']['fechahasta'] = fechahasta
        report['params']['WHERE'] = oParam['where']
        report['disposition'] = "inline"
        return report

    def sanhigia_informes_dameParamInforme(self, model):
        oParamInforme = {}
        oParamInforme['where'] = ""
        if model.i_facturascli_codagente and model.i_facturascli_codagente.codagente != "":
            if oParamInforme['where'] != "":
                oParamInforme['where'] += " AND "
            oParamInforme['where'] += "facturascli.codagente = '" + str(model.i_facturascli_codagente.codagente) + "'"
        if model.d_facturascli_fecha and model.d_facturascli_fecha != "":
            if oParamInforme['where'] != "":
                oParamInforme['where'] += " AND "
            oParamInforme['where'] += "facturascli.fecha >= '" + str(model.d_facturascli_fecha) + "'"
        if model.h_facturascli_fecha and model.h_facturascli_fecha != "":
            if oParamInforme['where'] != "":
                oParamInforme['where'] += " AND "
            oParamInforme['where'] += "facturascli.fecha <= '" + str(model.h_facturascli_fecha) + "'"
        print("WHERE_______________: " + oParamInforme['where'])
        return oParamInforme

    def __init__(self, context=None):
        super().__init__(context)

    def field_nombreagente(self, model):
        return self.ctx.sanhigia_informes_field_nombreagente(model)

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
