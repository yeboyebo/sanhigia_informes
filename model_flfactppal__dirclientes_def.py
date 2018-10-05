
# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *


class sanhigia_informes(alta_clientes):

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
        desc = "descripcion"
        return desc

    def sanhigia_informes_getDireccion(self, model, oParam):
        data = []

        print("getDireccion__Inicio")
        codcliente = oParam['codcliente']
        print("codcliente: ", codcliente)
        if codcliente:
            q = qsatype.FLSqlQuery()
            q.setTablesList(u"dirclientes")
            q.setSelect("id, descripcion")
            q.setFrom("dirclientes")

            q.setWhere(ustr(u"codcliente = '", codcliente, u"' ORDER BY id"))

            if not q.exec_():
                print("Error inesperado")
                return []

            while q.next():
                data.append({"id": str(q.value(0)), "descripcion": str(q.value(1))})
        print("getDireccion__Fin-data:", data)

        return data

    def sanhigia_informes_iniciaValoresCursor(self, cursor=None):
        print("¿¿¿¿¿")
        cursor.setValueBuffer(u"domfacturacion", True)
        cursor.setValueBuffer(u"domenvio", True)
        qsatype.FactoriaModulos.get('formRecorddirclientes').iface.iniciaValoresCursor(cursor)
        return True

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

    def getDireccion(self, model, oParam):
        return self.ctx.sanhigia_informes_getDireccion(model, oParam)

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.sanhigia_informes_iniciaValoresCursor(cursor)

