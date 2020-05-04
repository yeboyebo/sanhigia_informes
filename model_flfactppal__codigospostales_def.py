# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *


class sanhigia_informes(interna):

    def sanhigia_informes_getDesc(self):
        return "codpostal"

    def __init__(self, context=None):
        super().__init__(context)

    def getDesc(self):
        return self.ctx.sanhigia_informes_getDesc()


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
