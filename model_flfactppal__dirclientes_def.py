
# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *


class sanhigia_informes(alta_clientes):

    def sanhigia_informes_getDireccion(self, model, oParam):
        data = []

        codcliente = oParam['codcliente']
        if codcliente:
            q = qsatype.FLSqlQuery()
            q.setTablesList(u"dirclientes")
            q.setSelect("id,ciudad,dirtipovia,direccion,dirnum")
            q.setFrom("dirclientes")

            q.setWhere(ustr(u"codcliente = '", codcliente, u"' ORDER BY id"))

            if not q.exec_():
                return []

            while q.next():
                ciudad = q.value(1)
                if ciudad is None:
                    ciudad = ""
                dirtipovia = q.value(2)
                if dirtipovia is None:
                    dirtipovia = ""
                direccion = q.value(3)
                if direccion is None:
                    direccion = ""
                dirnum = q.value(4)
                if dirnum is None:
                    dirnum = ""
                descripcion = str(ciudad) + ", " + str(dirtipovia) + " " + str(direccion) + " " + str(dirnum)
                data.append({"id": str(q.value(0)), "descripcion": descripcion})

        return data

    def __init__(self, context=None):
        super().__init__(context)

    def getDireccion(self, model, oParam):
        return self.ctx.sanhigia_informes_getDireccion(model, oParam)

