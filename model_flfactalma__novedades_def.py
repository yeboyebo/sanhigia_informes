# @class_declaration interna #
from YBLEGACY import qsatype
from YBUTILS import gesDoc

class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *


class sanhigia_informes(interna):

    def sanhigia_informes_getDesc(self):
        return None

    def sanhigia_informes_getForeignFields(self, model, template=None):
        fields = []
        if template == "master":
            fields = [{'verbose_name': 'rowColor', 'func': 'field_colorRow'}]
        else:
            fields = [{'verbose_name': 'adjunto', 'func': 'field_adjunto'}]
        return fields

    def sanhigia_informes_field_adjunto(self, model):
        nombre = None
        file = gesDoc.getFiles("novedades", model.pk)
        if file:
            return file["nombre"]
        return nombre

    def sanhigia_checkButtonDescarga(self, cursor):
        file = gesDoc.getFiles("novedades", cursor.valueBuffer("codnovedad"))
        if file:
            return None
        return "disabled"

    def sanhigia_informes_field_colorRow(self, model):
        if model.tipo == "Novedad":
            #return "cSuccess"
            return "cInfo"
            #return "cWarning"
        if model.tipo == "Oferta":
            #return "cPrimary"
            return "cWarning"
            #return "cLink"
        else:
            return None

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.sanhigia_informes_getDesc()

    def getForeignFields(self, model, template=None):
        return self.ctx.sanhigia_informes_getForeignFields(model, template)

    def field_adjunto(self, model):
        return self.ctx.sanhigia_informes_field_adjunto(model)

    def checkButtonDescarga(self, cursor):
        return self.ctx.sanhigia_checkButtonDescarga(cursor)

    def field_colorRow(self, model):
        return self.ctx.sanhigia_informes_field_colorRow(model)


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
