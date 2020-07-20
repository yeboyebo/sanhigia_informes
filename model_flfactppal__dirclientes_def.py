
# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *
import datetime
from datetime import date
import calendar
import math

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

    def sanhigia_informes_calculaDatosMapaDirecciones(self, oParam):
        print(oParam)
        mapa = {}
        mapa["locations"] = []
        having = ""
        lineas = ""
        where = "d.geo_estadogeo = 'OK'"
        whereLatitudLongitud = "d.geo_estadogeo = 'OK'"
        whereReferencias =""
        hoy = date.today()
        ultimo = calendar.monthrange(hoy.year,hoy.month)[1]
        usuario = qsatype.FLUtil.nameUser()
        codAgente = qsatype.FLUtil.sqlSelect(u"agentes a INNER JOIN usuarios u ON a.idusuario = u.idusuario", u"codagente", ustr(u"u.idusuario = '", usuario, u"'"))
        if not codAgente:
            codAgente = '-1'

        if not oParam:
            mapa["locations"] = [
                ["Pol. ind. Lastra Monegros", 41.482558, -0.151526, "blue"]
            ]
            mapa["center"] = {"lat": 41.482558, "lng": -0.151526}
            where += " AND f.fecha BETWEEN '{}-01-01' AND '{}-{}-{}'".format(str(hoy.year), str(hoy.year), str(hoy.month), str(ultimo))
            return mapa

        if oParam:
            if "codcliente" in oParam:
                whereLatitudLongitud += " AND d.codcliente =  '{}'".format(oParam["codcliente"])

                latitud = qsatype.FLUtil.sqlSelect("dirclientes d", "DISTINCT(d.geo_latitud)", whereLatitudLongitud + " AND d.domfacturacion=true")
                longitud = qsatype.FLUtil.sqlSelect("dirclientes d", "DISTINCT(d.geo_longitud)", whereLatitudLongitud + "AND d.domfacturacion=true")
                direccion = qsatype.FLUtil.sqlSelect("dirclientes d", "d.direccion", "d.codcliente =  '" + oParam["codcliente"] + "' AND d.domfacturacion=true")

                idDireccion = qsatype.FLUtil.sqlSelect("dirclientes d", "d.id", "d.codcliente =  '" + oParam["codcliente"] + "' AND d.domfacturacion=true")

                nombre = qsatype.FLUtil.sqlSelect("clientes c", "c.nombre", "c.codcliente =  '" + oParam["codcliente"] + "'")

                if latitud == None and longitud == None:
                    # Aquí debe de dar un error o alerta
                    mapa = {}
                    mapa['status'] = 1
                    mapa['radio'] = 0
                    mapa['msg'] = "No hay coordenadas para la dirección {}".format(direccion)
                    mapa["locations"] = [
                        ["Pol. ind. Lastra Monegros", 41.482558, -0.151526, "blue"]
                    ]
                    mapa["center"] = {"lat": 41.482558, "lng": -0.151526}
                    return mapa
                else:
                    totalNeto = 0

                    mapa["center"] = {"lat": latitud, "lng": longitud}

                    otros = qsatype.FLUtil.sqlSelect("dirclientes d", "d.dirotros", "d.codcliente =  '" + oParam["codcliente"] + "' AND d.domfacturacion=true")

                    if "d_fechainicio" not in oParam and "h_fechainicio" not in oParam and "fecha" not in oParam:
                        totalNeto = qsatype.FLUtil.sqlSelect("facturascli f", "SUM(f.neto)", "f.codcliente = '" + oParam["codcliente"] + "'")
                    else:
                        if "d_fechainicio" in oParam:
                            totalNeto = qsatype.FLUtil.sqlSelect("facturascli f", "SUM(f.neto)", "f.codcliente = '" + oParam["codcliente"] + "' AND f.fecha BETWEEN '" + oParam["d_fechainicio"] + "' AND '" + oParam["h_fechainicio"] + "'")
                        if "fecha" in oParam:
                            totalNeto = qsatype.FLUtil.sqlSelect("facturascli f", "SUM(f.neto)", "f.codcliente = '" + oParam["codcliente"] + "' AND f.fecha = '" + oParam["fecha"] + "'")
                    if(totalNeto == None):
                        totalNeto = 0

                    if(otros == None):
                        labelCentro = "<strong>"+nombre+"</strong>"+"<br>"+direccion+"<br> Facturación total: "+str(qsatype.FLUtil.formatoMiles(totalNeto))+" €"
                    else:
                        labelCentro = "<strong>"+nombre+"</strong>"+"<br>"+direccion+" "+otros+"<br> Facturación total: "+str(qsatype.FLUtil.formatoMiles(totalNeto))+" €"
                    latitudCentro = latitud
                    longitudCentro = longitud
            else:
                latitud = 41.482558
                longitud = -0.151526
                mapa["locations"] = [
                        ["Pol. ind. Lastra Monegros", latitud, longitud, "blue"]
                    ]
                mapa["center"] = {"lat": latitud, "lng": longitud}
                mapa["msg"] = "Debe indicar un cliente"
                return mapa
            if "d_fechainicio" not in oParam and "h_fechainicio" not in oParam and "fecha" not in oParam:
                where += ""
            else:
                if "d_fechainicio" in oParam:
                    where += " AND f.fecha BETWEEN ' {} ' AND ' {} '".format(oParam["d_fechainicio"], oParam["h_fechainicio"])
                if "fecha" in oParam:
                    where += "AND f.fecha = '{}'".format(oParam["fecha"])

            if "zoom" in oParam:
                radio = int(math.pow(10,(((oParam["zoom"] - 16) * math.log(2,10))*-1)))
                print("radio: ", radio)

                latitudT = latitud + (int(radio)/110.57)
                latitudT = round(latitudT,6)

                latitud = latitud - (int(radio)/110.57)

                longitudT = longitud + (int(radio)/111.32)
                longitudT = round(longitudT,6)

                longitud = longitud -(int(radio)/111.32)

                where += " AND d.geo_latitud BETWEEN "+str(latitud)+" AND "+str(latitudT)+ "AND d.geo_longitud BETWEEN "+str(longitud)+" AND "+str(longitudT)

                if idDireccion and idDireccion != None:
                    where += " AND d.id <> " + str(idDireccion)
                    print("where: ", where)

                # + "OR d.geo_latitud=" + str(latitud) + " AND d.geo_longitud = "+ str(longitud)
            # if "radio" in oParam:
            #     latitudT = latitud + (int(oParam["radio"])/110.57)
            #     latitudT = round(latitudT,6)

            #     latitud = latitud - (int(oParam["radio"])/110.57)

            #     longitudT = longitud + (int(oParam["radio"])/111.32)
            #     longitudT = round(longitudT,6)

            #     longitud = longitud -(int(oParam["radio"])/111.32)

            #     where += " AND d.geo_latitud BETWEEN "+str(latitud)+" AND "+str(latitudT)+ "AND d.geo_longitud BETWEEN "+str(longitud)+" AND "+str(longitudT)# + "OR d.geo_latitud=" + str(latitud) + " AND d.geo_longitud = "+ str(longitud)

            # else:
            #     latitudT = latitud+(1/110.57)
            #     latitudT = round(latitudT,6)

            #     longitudT = longitud+(1/111.32)
            #     longitudT = round(longitudT,6)

            #     where += " AND d.geo_latitud BETWEEN "+str(latitud)+" AND "+str(latitudT)+ " AND d.geo_longitud BETWEEN "+str(longitud)+" AND "+str(longitudT) #+ "OR d.geo_latitud=" + str(latitud) + " AND d.geo_longitud = "+ str(longitud)

            if "facturacion" in oParam:
                minimo = float(oParam["facturacion"])
                having = " HAVING SUM(f.neto) > {}".format(oParam["facturacion"])
            else:
                minimo = float(200)
                having = " HAVING SUM(f.neto) >= 200"

            if "referencia_1" in oParam or "referencia_2" in oParam or "referencia_3" in oParam:
                referencias = []
                separador = ","
                lineas += "INNER JOIN lineasfacturascli l ON f.idfactura = l.idfactura"
                if "referencia_1" in oParam:
                    referencias.append("'"+oParam["referencia_1"]+"'")
                if "referencia_2" in oParam:
                    referencias.append("'"+oParam["referencia_2"]+"'")
                if "referencia_3" in oParam:
                    referencias.append("'"+oParam["referencia_3"]+"'")

                where += " AND l.referencia IN ({})".format(separador.join(referencias))

        if codAgente != '-1':
            where += " AND c.codagente = '{}'".format(codAgente)

        q = qsatype.FLSqlQuery()
        q.setTablesList("dirclientes, facturascli, clientes")
        q.setSelect("d.geo_latitud, d.direccion, d.geo_longitud, c.nombre, SUM(f.neto), d.dirotros, d.dirnum, f.codcliente")
        q.setFrom("dirclientes d INNER JOIN clientes c ON d.codcliente = c.codcliente INNER JOIN facturascli f ON c.codcliente = f.codcliente {}".format(lineas))
        q.setWhere("{} GROUP BY f.codcliente, d.id, c.codcliente, d.geo_latitud, d.direccion, geo_longitud, c.nombre, d.dirotros,d.dirnum {} ORDER BY SUM(f.neto) DESC LIMIT 50".format(where, having))
        print("sql: ", q.sql())
        if not q.exec_():
            return []
        resultados = q.size()
        cambio = int(resultados / 5)
        contador = 1
        print("resultado: ", resultados)
        print("cambio: ", cambio)
        if cambio < 1:
            cambio = 1
        while q.next():
            ultimaCompra = qsatype.FLUtil.sqlSelect(u"facturascli", u"fecha", ustr(u"codcliente = '",q.value(7) , u"' order by fecha desc"))
            totalNeto = q.value(4)
            totalNeto = qsatype.FLUtil.roundFieldValue(totalNeto, "facturascli", "neto")
            if(q.value(6) == None):
                if(q.value(5) == None):
                    label = "<strong>"+q.value(3)+"</strong>"+"<br>"+q.value(1)+"<br> Facturación total: "+str(qsatype.FLUtil.formatoMiles(totalNeto))+" €<br>Última compra: " + qsatype.FLUtil.dateAMDtoDMA(str(ultimaCompra))
                else:
                    label = "<strong>"+q.value(3)+"</strong>"+"<br>"+q.value(1)+" "+q.value(5)+"<br> Facturación total: "+str(qsatype.FLUtil.formatoMiles(totalNeto))+" €<br>Última compra: " + qsatype.FLUtil.dateAMDtoDMA(str(ultimaCompra))
            else:
                if(q.value(5) == None):
                    label = "<strong>"+q.value(3)+"</strong>"+"<br>"+q.value(1)+" Nº "+q.value(6)+"<br> Facturación total: "+str(qsatype.FLUtil.formatoMiles(totalNeto))+" €<br>Última compra: " + qsatype.FLUtil.dateAMDtoDMA(str(ultimaCompra))
                else:
                    label = "<strong>"+q.value(3)+"</strong>"+"<br>"+q.value(1)+" Nº "+q.value(6)+ " - "+q.value(5)+"<br> Facturación total: "+str(qsatype.FLUtil.formatoMiles(totalNeto))+" €<br>Última compra: " + qsatype.FLUtil.dateAMDtoDMA(str(ultimaCompra))
            if contador >= cambio * 5:
                mapa["locations"].append([label, q.value(0), q.value(2), "yellow_light"])
            elif contador >= cambio * 4:
                mapa["locations"].append([label, q.value(0), q.value(2), "yellow"])
            elif contador >= cambio * 3:
                mapa["locations"].append([label, q.value(0), q.value(2), "orange_light"])
            elif contador >= cambio * 2:
                mapa["locations"].append([label, q.value(0), q.value(2), "orange"])
            elif contador >= cambio:
                mapa["locations"].append([label, q.value(0), q.value(2), "red"])
            # if(float(totalNeto) < float((minimo + (minimo * 25 / 100)))):
            #     mapa["locations"].append([label, q.value(0), q.value(2), "yellow_light"])
            # elif(float(totalNeto) < float((minimo + (minimo * 50 / 100)))):
            #     mapa["locations"].append([label, q.value(0), q.value(2), "yellow"])
            # elif(float(totalNeto) < float((minimo + (minimo * 75 / 100)))):
            #     mapa["locations"].append([label, q.value(0), q.value(2), "orange_light"])
            # elif(float(totalNeto) < float((minimo * 2))):
            #     mapa["locations"].append([label, q.value(0), q.value(2), "orange"])
            # else:
            #     mapa["locations"].append([label, q.value(0), q.value(2), "red"])
            contador += 1
            # if(q.value(0) == mapa["center"]["lat"] and q.value(2) == mapa["center"]["lng"]):
            #     mapa["locations"].append([label, q.value(0), q.value(2), "blue"])
            # else:
            #     mapa["locations"].append([label, q.value(0), q.value(2), "red"])
        mapa["locations"].append([labelCentro, latitudCentro, longitudCentro, "blue"])
        mapa["zoom"] = oParam["zoom"]
        return mapa

    # def sanhigia_informes_validateCursor(self, cursor):
    #     telefono = cursor.valueBuffer("telefono")
    #     if not telefono:
    #         qsatype.FLUtil.ponMsgError("El campo Teléfono no esta informado. Por favor, selecciona un teléfono valido.")
    #         return False
    #     return True

    def sanhigia_informes_generaMapaDirecciones(self, model, template):
        return self.iface.calculaDatosMapaDirecciones({})

    def sanhigia_informes_getMapaDirecciones(self, oParam):
        return self.iface.calculaDatosMapaDirecciones(oParam)

    def __init__(self, context=None):
        super().__init__(context)

    def getDireccion(self, model, oParam):
        return self.ctx.sanhigia_informes_getDireccion(model, oParam)

    def generaMapaDirecciones(self, model, template):
        return self.ctx.sanhigia_informes_generaMapaDirecciones(model, template)

    def getMapaDirecciones(self, oParam):
        return self.ctx.sanhigia_informes_getMapaDirecciones(oParam)

    def calculaDatosMapaDirecciones(self, oParam):
        return self.ctx.sanhigia_informes_calculaDatosMapaDirecciones(oParam)

    # def validateCursor(self, cursor):
    #     return self.ctx.sanhigia_informes_validateCursor(cursor)

