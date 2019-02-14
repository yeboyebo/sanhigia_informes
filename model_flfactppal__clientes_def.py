
# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *
from YBUTILS.viewREST import cacheController


class sanhigia_informes(alta_clientes):

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
                cacheController.setSessionVariable(ustr(u"referencia2_", qsatype.FLUtil.nameUser()), filters['[referencia_2]'])
                ref2 = "'" + cacheController.getSessionVariable(ustr(u"referencia2_", qsatype.FLUtil.nameUser())) + "'"
            if("[referencia_3]" in filters and filters['[referencia_3]'] != ''):
                print("Hay referencia")
                cacheController.setSessionVariable(ustr(u"referencia3_", qsatype.FLUtil.nameUser()), filters['[referencia_3]'])
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
        if cacheController.getSessionVariable(ustr(u"referencia2_", qsatype.FLUtil.nameUser())):
            cacheController.dropSessionVariable(ustr(u"referencia2_", qsatype.FLUtil.nameUser()))
        if cacheController.getSessionVariable(ustr(u"referencia3_", qsatype.FLUtil.nameUser())):
            cacheController.dropSessionVariable(ustr(u"referencia3_", qsatype.FLUtil.nameUser()))
        if cacheController.getSessionVariable(ustr(u"fecha1_", qsatype.FLUtil.nameUser())):
            cacheController.dropSessionVariable(ustr(u"fecha1_", qsatype.FLUtil.nameUser()))
        return initFilter

    def sanhigia_informes_queryGrid_ventasClientes(self, model, filters):
        ref1 = ''
        ref2 = ''
        ref3 = ''
        masWhere = ''
        print("-----------------------------------cliente: " + model.codcliente)
        if not cacheController.getSessionVariable(ustr(u"referencia1_", qsatype.FLUtil.nameUser())):
            pass
        else:
            ref1 = "'" + cacheController.getSessionVariable(ustr(u"referencia1_", qsatype.FLUtil.nameUser())) + "'"
            if ref1 != '':
                masWhere = " AND (lineaspedidoscli.referencia = " + ref1
        if not cacheController.getSessionVariable(ustr(u"referencia2_", qsatype.FLUtil.nameUser())):
            pass
        else:
            ref2 = "'" + cacheController.getSessionVariable(ustr(u"referencia2_", qsatype.FLUtil.nameUser())) + "'"
            if ref2 != '':
                if masWhere != '':
                    masWhere = masWhere + " OR lineaspedidoscli.referencia = " + ref2
                else:
                    masWhere = " AND (lineaspedidoscli.referencia = " + ref2
        if not cacheController.getSessionVariable(ustr(u"referencia3_", qsatype.FLUtil.nameUser())):
            pass
        else:
            ref3 = "'" + cacheController.getSessionVariable(ustr(u"referencia3_", qsatype.FLUtil.nameUser())) + "'"
            if ref3 != '':
                if masWhere != '':
                    masWhere = masWhere + " OR lineaspedidoscli.referencia = " + ref3
                else:
                    masWhere = " AND (lineaspedidoscli.referencia = " + ref3
        if masWhere != '':
            masWhere = masWhere + ')'
        print("---------------mashwere: " + masWhere)
        query = {}
        query["tablesList"] = ("pedidoscli,lineaspedidoscli")
        query["select"] = ("lineaspedidoscli.referencia, lineaspedidoscli.descripcion, lineaspedidoscli.cantidad, lineaspedidoscli.pvpunitario, lineaspedidoscli.dtopor, pedidoscli.fecha, lineaspedidoscli.pvptotal, pedidoscli.codigo")
        query["from"] = ("pedidoscli INNER JOIN lineaspedidoscli ON pedidoscli.idpedido = lineaspedidoscli.idpedido")
        query["where"] = ("pedidoscli.codcliente = '" + str(model.codcliente) + "'" + masWhere)
        query["orderby"] = "pedidoscli.fecha DESC"
        return query

    def sanhigia_informes_queryGrid_clientesNuevos(self, model, filters):
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
                cacheController.setSessionVariable(ustr(u"referencia2_", qsatype.FLUtil.nameUser()), filters['[referencia_2]'])
                ref2 = "'" + cacheController.getSessionVariable(ustr(u"referencia2_", qsatype.FLUtil.nameUser())) + "'"
            if("[referencia_3]" in filters and filters['[referencia_3]'] != ''):
                print("Hay referencia")
                cacheController.setSessionVariable(ustr(u"referencia3_", qsatype.FLUtil.nameUser()), filters['[referencia_3]'])
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
        query["select"] = ("c.codcliente, c.nombre, c.email, c.telefono1, MIN(antes.fecha) as fecha, (d.dirtipovia || ' ' || d.direccion || ' ' || d.dirnum || ' - ' || d.ciudad || ' ' || d.codpostal) as direc")
        query["from"] = ("clientes AS c INNER JOIN pedidoscli AS antes ON c.codcliente = antes.codcliente AND antes.fecha >= " + fecha + " LEFT OUTER JOIN pedidoscli AS despues ON c.codcliente = despues.codcliente AND despues.fecha < " + fecha + " INNER JOIN dirclientes d ON c.codcliente = d.codcliente and d.domfacturacion is true INNER JOIN lineaspedidoscli ON antes.idpedido = lineaspedidoscli.idpedido")
        query["where"] = "antes.codcliente IS NOT NULL and despues.codcliente IS NULL" + masWhere
        query["groupby"] = " c.codcliente, c.nombre, c.email, c.telefono1, (d.dirtipovia || ' ' || d.direccion || ' ' || d.dirnum || ' - ' || d.ciudad || ' ' || d.codpostal)"
        query["orderby"] = "c.nombre DESC"
        return query

    def sanhigia_informes_queryGrid_comparativas(self, model, filters):
        trimestre = ''
        anio1 = ''
        anio2 = ''
        anio1f = ''
        anio2f = ''
        where = "1 = 1"
        masWhere = ""
        if(filters):
            if filters['[trimestre]'] and filters['[trimestre]'] != "":
                # trimestre = filters['[trimestre]']
                print(filters['[trimestre]'])
                cacheController.setSessionVariable(ustr(u"trimestre_", qsatype.FLUtil.nameUser()), filters['[trimestre]'])
                trimestre = "'" + cacheController.getSessionVariable(ustr(u"trimestre_", qsatype.FLUtil.nameUser())) + "'"
                print(trimestre)
            if filters['[anio_1]'] and filters['[anio_1]'] != "":
                print("anio1-1: " + filters['[anio_1]'])
                print("TRIMESTRE: " + trimestre)
                if trimestre == "":
                    print("anio1: " + filters['[anio_1]'])
                    anio1 = "'" + filters['[anio_1]'] + "-01-01'"
                    anio1f = "'" + filters['[anio_1]'] + "-12-31'"
                elif trimestre == "'T1'":
                    anio1 = "'" + filters['[anio_1]'] + "-01-01'"
                    anio1f = "'" + filters['[anio_1]'] + "-03-31'"
                elif trimestre == "'T2'":
                    anio1 = "'" + filters['[anio_1]'] + "-04-01'"
                    anio1f = "'" + filters['[anio_1]'] + "-06-30'"
                elif trimestre == "'T3'":
                    anio1 = "'" + filters['[anio_1]'] + "-07-01'"
                    anio1f = "'" + filters['[anio_1]'] + "-09-30'"
                elif trimestre == "'T4'":
                    anio1 = "'" + filters['[anio_1]'] + "-10-01'"
                    anio1f = "'" + filters['[anio_1]'] + "-12-31'"
                cacheController.setSessionVariable(ustr(u"anio1_", qsatype.FLUtil.nameUser()), anio1)
                cacheController.setSessionVariable(ustr(u"anio1f_", qsatype.FLUtil.nameUser()), anio1f)
            if filters['[anio_2]'] and filters['[anio_2]'] != "":
                print("anio2-2: " + filters['[anio_2]'])
                print("TRIMESTRE 2: " + trimestre)
                if trimestre == "":
                    print("anio2: " + filters['[anio_2]'])
                    anio2 = "'" + filters['[anio_2]'] + "-01-01'"
                    anio2f = "'" + filters['[anio_2]'] + "-12-31'"
                elif trimestre == "'T1'":
                    anio2 = "'" + filters['[anio_2]'] + "-01-01'"
                    anio2f = "'" + filters['[anio_2]'] + "-03-31'"
                elif trimestre == "'T2'":
                    anio2 = "'" + filters['[anio_2]'] + "-04-01'"
                    anio2f = "'" + filters['[anio_2]'] + "-06-30'"
                elif trimestre == "'T3'":
                    anio2 = "'" + filters['[anio_2]'] + "-07-01'"
                    anio2f = "'" + filters['[anio_2]'] + "-09-30'"
                elif trimestre == "'T4'":
                    anio2 = "'" + filters['[anio_2]'] + "-10-01'"
                    anio2f = "'" + filters['[anio_2]'] + "-12-31'"
                cacheController.setSessionVariable(ustr(u"anio2_", qsatype.FLUtil.nameUser()), anio2)
                cacheController.setSessionVariable(ustr(u"anio2f_", qsatype.FLUtil.nameUser()), anio2f)
            print(anio1f)
            print(anio2f)
        if not anio1 or anio1 == "''":
            anio1 = "'2100-01-01'"
            anio1f = "'2100-01-01'"
            where = "1 = 2"
        if not anio2 or anio2 == "''":
            anio2 = "'2100-01-01'"
            anio2f = "'2100-01-01'"
            where = "1 = 2"
        print('Seguimos con la query')
        usuario = qsatype.FLUtil.nameUser()
        codGrupo = qsatype.FLUtil.sqlSelect(u"flusers", u"idgroup", ustr(u"iduser = '", usuario, u"' AND idgroup = 'Administracion'"))
        if not codGrupo:
            codagente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
            masWhere = u" AND clientes.codagente = '" + str(codagente) + "'"
        query = {}
        # Ya está, a AQNext no le había gustado que pusieses dos "as" en el mismo campo, porque no podía sacar bien el alias y eso. He hecho el cast con "::numeric" y he cambiado el nombre del campo en los json (estaba con c.codcliente) y ya va. Comprueba que no me haya cargado nada.
        # query["tablesList"] = ("clientes,pedidoscli")
        # query["select"] = ("clientes.codcliente, clientes.nombre, clientes.email, clientes.telefono1, COALESCE(SUM(f.total),0) as total1, dirclientes.direccion, COALESCE(SUM(f2.total),0) as total2, CASE WHEN COALESCE(SUM(f.total),0) = 0 THEN (CASE WHEN COALESCE(SUM(f2.total),0) = 0 THEN 0 ELSE 100 END) ELSE round(((((COALESCE(SUM(f2.total),0) - COALESCE(SUM(f.total),0)) * 100)) / COALESCE(SUM(f.total),0))::numeric,2) END as variacion")
        # query["from"] = ("clientes LEFT OUTER JOIN pedidoscli f ON clientes.codcliente = f.codcliente AND f.fecha BETWEEN " + anio1 + " AND " + anio1f + " LEFT OUTER JOIN pedidoscli f2 ON clientes.codcliente = f2.codcliente AND f2.fecha BETWEEN " + anio2 + " AND " + anio2f + " INNER JOIN dirclientes ON clientes.codcliente = dirclientes.codcliente and dirclientes.domfacturacion is true")
        # query["where"] = where
        # query["groupby"] = " clientes.codcliente, clientes.nombre, clientes.email, clientes.telefono1, dirclientes.direccion"
        # query["orderby"] = "clientes.nombre DESC"

        query["tablesList"] = ("clientes,dirclientes")
        query["select"] = ("clientes.codcliente, clientes.nombre, clientes.email, clientes.telefono1, dirclientes.direccion, (SELECT COALESCE(SUM(pedidoscli.total),0) from pedidoscli  where pedidoscli.codcliente = clientes.codcliente and pedidoscli.fecha BETWEEN " + anio1 + " AND " + anio1f + ") AS total1, (SELECT COALESCE(SUM(pedidoscli.total),0) from pedidoscli  where pedidoscli.codcliente = clientes.codcliente and pedidoscli.fecha BETWEEN " + anio2 + " AND " + anio2f + ") AS total2, CASE WHEN (SELECT COALESCE(SUM(pedidoscli.total),0) from pedidoscli  where pedidoscli.codcliente = clientes.codcliente and pedidoscli.fecha BETWEEN " + anio1 + " AND " + anio1f + ") = 0 THEN (CASE WHEN (SELECT COALESCE(SUM(pedidoscli.total),0) from pedidoscli  where pedidoscli.codcliente = clientes.codcliente and pedidoscli.fecha BETWEEN " + anio2 + " AND " + anio2f + ") = 0 THEN 0 ELSE 100 END) ELSE round((((((SELECT COALESCE(SUM(pedidoscli.total),0) from pedidoscli  where pedidoscli.codcliente = clientes.codcliente and pedidoscli.fecha BETWEEN " + anio2 + " AND " + anio2f + ") - (SELECT COALESCE(SUM(pedidoscli.total),0) from pedidoscli  where pedidoscli.codcliente = clientes.codcliente and pedidoscli.fecha BETWEEN " + anio1 + " AND " + anio1f + ")) * 100)) / (SELECT COALESCE(SUM(pedidoscli.total),0) from pedidoscli  where pedidoscli.codcliente = clientes.codcliente and pedidoscli.fecha BETWEEN " + anio1 + " AND " + anio1f + "))::numeric,2) END AS variacion")
        query["from"] = ("clientes INNER JOIN dirclientes ON clientes.codcliente = dirclientes.codcliente and dirclientes.domfacturacion is true INNER JOIN pedidoscli ON clientes.codcliente = pedidoscli.codcliente")
        query["where"] = (where + masWhere + " AND ((pedidoscli.fecha BETWEEN " + anio1 + " AND " + anio1f + ") OR (pedidoscli.fecha BETWEEN " + anio2 + " AND " + anio2f + "))")
        query["groupby"] = ("clientes.codcliente, clientes.nombre, clientes.email, clientes.telefono1, dirclientes.direccion")
        query["orderby"] = ("clientes.nombre DESC")
        return query

    def __init__(self, context=None):
        super().__init__(context)

    def getFilters(self, model, name, template=None):
        return self.ctx.sanhigia_informes_getFilters(model, name, template)

    def getCliente(self, model, oParam):
        return self.ctx.sanhigia_informes_getCliente(model, oParam)

    def iniciaValoresCursor(self, cursor=None):
        return self.ctx.sanhigia_informes_iniciaValoresCursor(cursor)

    def queryGrid_clientesInactivos(self, model, filters):
        return self.ctx.sanhigia_informes_queryGrid_clientesInactivos(model, filters)

    def queryGrid_clientesInactivos_initFilter(self):
        return self.ctx.sanhigia_informes_queryGrid_clientesInactivos_initFilter()

    def queryGrid_ventasClientes(self, model, filters):
        return self.ctx.sanhigia_informes_queryGrid_ventasClientes(model, filters)

    def queryGrid_clientesNuevos(self, model, filters):
        return self.ctx.sanhigia_informes_queryGrid_clientesNuevos(model, filters)

    def queryGrid_comparativas(self, model, filters):
        return self.ctx.sanhigia_informes_queryGrid_comparativas(model, filters)

