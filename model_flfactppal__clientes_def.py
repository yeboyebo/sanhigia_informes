
# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *
from YBUTILS.viewREST import cacheController


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
        if name == 'clientesUsuario':
            usuario = qsatype.FLUtil.nameUser()
            codGrupo = qsatype.FLUtil.sqlSelect(u"flusers", u"idgroup", ustr(u"iduser = '", usuario, u"' AND idgroup = 'Administracion'"))
            if codGrupo:
                return filters
            else:
                codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
                if not codagente:
                    codagente = '-1'
                return [{'criterio': 'codagente__exact', 'valor': codagente}]
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

    def sanhigia_informes_iniciaValoresCursor(self, cursor=None):
        usuario = qsatype.FLUtil.nameUser()
        codGrupo = qsatype.FLUtil.sqlSelect(u"flusers", u"idgroup", ustr(u"iduser = '", usuario, u"' AND idgroup = 'Administracion'"))
        if codGrupo:
            codagente = ''
        else:
            codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
            if not codagente:
                codagente = ''
        cursor.setValueBuffer(u"codagente", codagente)
        '''
        codCliente = qsatype.FLUtil.sqlSelect(u"clientes", u"codcliente", ustr(u"codcliente = '", cursor.valueBuffer("codcliente"), u"'"))
        if codCliente:
            response = {}
            response['status'] = 1
            response['msg'] = "Error: El codigo es valor unico. Hay otro registro con codigo " + cursor.valueBuffer("codcliente") + "."
        '''
        qsatype.FactoriaModulos.get('formRecordclientes').iface.iniciaValoresCursor(cursor)
        return True

    def sanhigia_informes_queryGrid_clientesInactivos(self, model, filters):
        fecha = "CURRENT_DATE"
        masWhere = ''
        ref = ''
        ref2 = ''
        ref3 = ''
        refs = ''
        if(filters):
            print(filters)
            if("[d_fecha]" in filters and filters['[d_fecha]'] != ''):
                print(filters['[d_fecha]'])
                #fecha = "'" + filters['[d_fecha]'] + "'"
                cacheController.setSessionVariable(ustr(u"fecha1_", qsatype.FLUtil.nameUser()), filters['[d_fecha]'])
                fecha = "'" + cacheController.getSessionVariable(ustr(u"fecha1_", qsatype.FLUtil.nameUser())) + "'"
            if("[referencia_1]" in filters and filters['[referencia_1]'] != ''):
                print("Hay referencia")
                cacheController.setSessionVariable(ustr(u"referencia1_", qsatype.FLUtil.nameUser()), filters['[referencia_1]'])
                ref = "'" + cacheController.getSessionVariable(ustr(u"referencia1_", qsatype.FLUtil.nameUser())) + "'"
            if("[referencia_2]" in filters and filters['[referencia_2]'] != ''):
                print("Hay referencia")
                cacheController.setSessionVariable(ustr(u"referencia2_", qsatype.FLUtil.nameUser()), filters['[referencia_1]'])
                ref2 = "'" + cacheController.getSessionVariable(ustr(u"referencia2_", qsatype.FLUtil.nameUser())) + "'"
            if("[referencia_3]" in filters and filters['[referencia_3]'] != ''):
                print("Hay referencia")
                cacheController.setSessionVariable(ustr(u"referencia3_", qsatype.FLUtil.nameUser()), filters['[referencia_1]'])
                ref3 = "'" + cacheController.getSessionVariable(ustr(u"referencia3_", qsatype.FLUtil.nameUser())) + "'"
        else:
            print("borrando variables de sesion")
            if cacheController.getSessionVariable(ustr(u"referencia1_", qsatype.FLUtil.nameUser())):
                cacheController.dropSessionVariable(ustr(u"referencia1_", qsatype.FLUtil.nameUser()))
            if cacheController.getSessionVariable(ustr(u"referencia2_", qsatype.FLUtil.nameUser())):
                cacheController.dropSessionVariable(ustr(u"referencia2_", qsatype.FLUtil.nameUser()))
            if cacheController.getSessionVariable(ustr(u"referencia3_", qsatype.FLUtil.nameUser())):
                cacheController.dropSessionVariable(ustr(u"referencia3_", qsatype.FLUtil.nameUser()))
            if cacheController.getSessionVariable(ustr(u"fecha1_", qsatype.FLUtil.nameUser())):
                cacheController.dropSessionVariable(ustr(u"fecha1_", qsatype.FLUtil.nameUser()))
        usuario = qsatype.FLUtil.nameUser()
        codGrupo = qsatype.FLUtil.sqlSelect(u"flusers", u"idgroup", ustr(u"iduser = '", usuario, u"' AND idgroup = 'Administracion'"))
        if not codGrupo:
            codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
            masWhere = u" AND c.codagente = '" + str(codagente) + "'"
        if ref != '':
            refs = u" AND lineaspedidoscli.referencia IN (" + str(ref)
        if ref2 != '':
            if refs != '':
                refs = refs + u"," + str(ref2)
            else:
                refs = u" AND lineaspedidoscli.referencia IN (" + str(ref2)
        if ref3 != '':
            if refs != '':
                refs = refs + u"," + str(ref3)
            else:
                refs = u" AND lineaspedidoscli.referencia IN (" + str(ref3)
        if refs != '':
            refs = refs + ")"
            masWhere = masWhere + refs
        print("____________ " + masWhere)
        query = {}
        query["tablesList"] = ("clientes,pedidoscli")
        query["select"] = ("c.codcliente, c.nombre, c.email, c.telefono1, MAX(antes.fecha) as fecha, (d.dirtipovia || ' ' || d.direccion || ' ' || d.dirnum || ' - ' || d.ciudad || ' ' || d.codpostal) as direc")
        query["from"] = ("clientes AS c INNER JOIN pedidoscli AS antes ON c.codcliente = antes.codcliente AND antes.fecha < " + fecha + " LEFT OUTER JOIN pedidoscli AS despues ON c.codcliente = despues.codcliente AND despues.fecha >= " + fecha + " INNER JOIN dirclientes d ON c.codcliente = d.codcliente and d.domfacturacion is true INNER JOIN lineaspedidoscli ON antes.idpedido = lineaspedidoscli.idpedido")
        query["where"] = "antes.codcliente IS NOT NULL and despues.codcliente IS NULL" + masWhere
        query["groupby"] = " c.codcliente, c.nombre, c.email, c.telefono1, (d.dirtipovia || ' ' || d.direccion || ' ' || d.dirnum || ' - ' || d.ciudad || ' ' || d.codpostal)"
        query["orderby"] = "c.nombre DESC"
        return query

    def sanhigia_informes_queryGrid_clientesInactivos_initFilter(self):
        initFilter = {}
        if cacheController.getSessionVariable(ustr(u"referencia1_", qsatype.FLUtil.nameUser())):
            cacheController.dropSessionVariable(ustr(u"referencia1_", qsatype.FLUtil.nameUser()))
        if cacheController.getSessionVariable(ustr(u"fecha1_", qsatype.FLUtil.nameUser())):
            cacheController.dropSessionVariable(ustr(u"fecha1_", qsatype.FLUtil.nameUser()))
        return initFilter

    def sanhigia_informes_queryGrid_ventasClientes(self, model):
        ref = ''
        masWhere = ''
        print("-----------------------------------cliente: " + model.codcliente)
        if not cacheController.getSessionVariable(ustr(u"referencia1_", qsatype.FLUtil.nameUser())):
            pass
        else:
            ref = "'" + cacheController.getSessionVariable(ustr(u"referencia1_", qsatype.FLUtil.nameUser())) + "'"
            if ref != '':
                masWhere = " AND lineaspedidoscli.referencia = " + ref
        print("---------------referencia: " + ref)
        query = {}
        query["tablesList"] = ("pedidoscli,lineaspedidoscli")
        query["select"] = ("lineaspedidoscli.referencia, lineaspedidoscli.descripcion, lineaspedidoscli.cantidad, lineaspedidoscli.pvpunitario, lineaspedidoscli.dtopor, pedidoscli.fecha, lineaspedidoscli.pvptotal, pedidoscli.codigo")
        query["from"] = ("pedidoscli INNER JOIN lineaspedidoscli ON pedidoscli.idpedido = lineaspedidoscli.idpedido")
        query["where"] = ("pedidoscli.codcliente = '" + str(model.codcliente) + "'" + masWhere)
        query["orderby"] = "pedidoscli.fecha DESC"
        return query

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

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.sanhigia_informes_iniciaValoresCursor(cursor)

    def queryGrid_clientesInactivos(self, model, filters):
        return self.ctx.sanhigia_informes_queryGrid_clientesInactivos(model, filters)

    def queryGrid_clientesInactivos_initFilter(self):
        return self.ctx.sanhigia_informes_queryGrid_clientesInactivos_initFilter()

    def queryGrid_ventasClientes(self, model):
        return self.ctx.sanhigia_informes_queryGrid_ventasClientes(model)

