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

    def sanhigia_informes_bChCursor(self, fN, cursor):
        # if not qsatype.FactoriaModulos.get('formRecordi_pedidoscli').iface.bChCursor(cursor):
        #     return False
        if fN == u"i_facturascli_codcliente":
            codagente = qsatype.FLUtil.sqlSelect(u"clientes", u"codagente", ustr(u"codcliente = '", cursor.valueBuffer(u"i_facturascli_codcliente"), u"'"))
            cursor.setValueBuffer("i_facturascli_codagente", codagente)

    def sanhigia_informes_getFilters(self, model, name, template=None):
        filters = []
        if name == 'filtroagente':
            usuario = qsatype.FLUtil.nameUser()
            if flfactinfo_def.iface.esadmin(usuario):
                return filters
            else:
                codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
                if not codagente:
                    codagente = '-1'
                return [{'criterio': 'i_facturascli_codagente__exact', 'valor': codagente}]
        return filters

    def sanhigia_informes_getForeignFields(self, model, template=None):
        fields = []
        if template == 'master':
            return [
                {'verbose_name': 'nombreagente', 'func': 'field_nombreagente'},
                {'verbose_name': 'nombrecliente', 'func': 'field_nombrecliente'}
            ]
        return fields

    def sanhigia_informes_field_nombreagente(self, model):
        try:
            return model.i_facturascli_codagente.nombreap
        except Exception:
            return ""

    def sanhigia_informes_field_nombrecliente(self, model):
        try:
            return model.i_facturascli_codcliente.nombre
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
        report['reportName'] = "i_sh_consumocliente"
        report['params'] = {}
        formato = "%d-%m-%Y"
        if model.i_facturascli_codagente and model.i_facturascli_codagente.nombreap != "":
            report['params']['nombreagente'] = model.i_facturascli_codagente.nombreap
        if model.i_facturascli_codcliente:
            if model.i_facturascli_codcliente.nombre != "":
                report['params']['nombrecliente'] = model.i_facturascli_codcliente.nombre
            if model.i_facturascli_codcliente.cifnif != "":
                report['params']['cifnif'] = model.i_facturascli_codcliente.cifnif
            direccion = _i.dameDireccionCliente(model.i_facturascli_codcliente.codcliente)
            if direccion != "":
                report['params']['direccion'] = direccion
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
        if model.i_facturascli_codcliente.codcliente and model.i_facturascli_codcliente.codcliente != "":
            if oParamInforme['where'] != "":
                oParamInforme['where'] += " AND "
            oParamInforme['where'] += "facturascli.codcliente = '" + str(model.i_facturascli_codcliente.codcliente) + "'"
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
        return oParamInforme

    def sanhigia_informes_dameDireccionCliente(self, codCliente):
        direccion = ""
        q = qsatype.FLSqlQuery()
        q.setSelect(u"dirtipovia,direccion,dirnum,dirotros,codpostal,ciudad,provincia")
        q.setFrom(u"dirclientes")
        q.setWhere(ustr(u"codcliente = '", codCliente, u"' AND domfacturacion"))
        if not q.exec_():
            return False
        if q.first():
            if q.value("dirtipovia") != "" and q.value("dirtipovia") is not None:
                direccion += q.value("dirtipovia") + " "
            if q.value("direccion") != "" and q.value("direccion") is not None:
                direccion += q.value("direccion") + " "
            if q.value("dirnum") != "" and q.value("dirnum") is not None:
                direccion += q.value("dirnum") + " "
            if q.value("dirotros") != "" and q.value("dirotros") is not None:
                direccion += q.value("dirotros") + " "
            if q.value("codpostal") != "" and q.value("codpostal") is not None:
                direccion += "," + q.value("codpostal") + " "
            if q.value("ciudad") != "" and q.value("ciudad") is not None:
                direccion += q.value("ciudad") + " "
            if q.value("provincia") != "" and q.value("provincia") is not None:
                direccion += q.value("provincia") + " "
        direccion = direccion[:-1]
        return direccion

    def __init__(self, context=None):
        super().__init__(context)

    def bChCursor(self, fN, cursor):
        return self.ctx.sanhigia_informes_bChCursor(fN, cursor)

    def field_nombreagente(self, model):
        return self.ctx.sanhigia_informes_field_nombreagente(model)

    def field_nombrecliente(self, model):
        return self.ctx.sanhigia_informes_field_nombrecliente(model)

    def getFilters(self, model, name, template=None):
        return self.ctx.sanhigia_informes_getFilters(model, name, template)

    def getForeignFields(self, model, template=None):
        return self.ctx.sanhigia_informes_getForeignFields(model, template)

    def getDesc(self):
        return self.ctx.sanhigia_informes_getDesc()

    def checkCodAgente(self, cursor):
        return self.ctx.sanhigia_informes_checkCodAgente(cursor)

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.sanhigia_informes_iniciaValoresCursor(cursor)

    def generarReport(self, model):
        return self.ctx.sanhigia_informes_generarReport(model)

    def dameParamInforme(self, model):
        return self.ctx.sanhigia_informes_dameParamInforme(model)

    def dameDireccionCliente(self, codCliente):
        return self.ctx.sanhigia_informes_dameDireccionCliente(codCliente)


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
