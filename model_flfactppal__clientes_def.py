# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *


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
        return filters

    def sanhigia_informes_getForeignFields(self, model, template=None):
        fields = []
        return fields

    def sanhigia_informes_getDesc(self):
        desc = "nombre"
        return desc

    def sanhigia_informes_getCliente(self, model, oParam):
        data = []
        usuario = qsatype.FLUtil.nameUser()
        codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
        if not codagente:
            codagente = '-1'

        q = qsatype.FLSqlQuery()
        q.setTablesList(u"clientes")
        q.setSelect("nombre, codcliente")
        q.setFrom("clientes")
        # q.setWhere("UPPER(nombre) LIKE '%" + oParam['val'].upper() + "%' OR UPPER(codcliente) LIKE '%" + oParam['val'].upper() + "%' OR UPPER(cifnif) LIKE '%" + oParam['val'].upper() + "%' OR codcliente in (SELECT cc.codcliente FROM contactosclientes cc INNER JOIN crm_contactos cr ON cc.codcontacto = cr.codcontacto WHERE UPPER(cr.nif) LIKE '%" + oParam['val'].upper() + "%')")
        print(oParam['val'])
        print(oParam)
        q.setWhere(ustr(u"codagente = '", codagente, u"' AND ((UPPER(nombre) LIKE '%" + oParam['val'].upper() + "%')" + " OR UPPER(codcliente) LIKE '%" + oParam['val'].upper() + "%') AND debaja = false"))

        if not q.exec_():
            print("Error inesperado")
            return []
        '''if q.size() > 200:
            return []'''

        while q.next():
            data.append({"nombre": q.value(0), "codcliente": q.value(1)})

        return data

    def __init__(self, context=None):
        super(sanhigia_informes, self).__init__(context)

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

    def getCliente(self, model, oParam):
        return self.ctx.sanhigia_informes_getCliente(model, oParam)


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
