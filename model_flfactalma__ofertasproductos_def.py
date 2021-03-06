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
        fields = [{'verbose_name': 'adjunto', 'func': 'field_adjunto'}]
        return fields

    def sanhigia_informes_field_adjunto(self, model):
        nombre = None
        file = gesDoc.getFiles("ofertasproductos", model.pk)
        if file:
            return file["nombre"]
        return nombre

    def sanhigia_checkButtonDescarga(self, cursor):
        file = gesDoc.getFiles("ofertasproductos", cursor.valueBuffer("idoferta"))
        if file:
            return None
        return "disabled"

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
