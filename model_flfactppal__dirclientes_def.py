
# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *


class sanhigia_informes(alta_clientes):

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

    def __init__(self, context=None):
        super().__init__(context)

    def getDireccion(self, model, oParam):
        return self.ctx.sanhigia_informes_getDireccion(model, oParam)

