# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context

# @class_declaration flfactinfo #
from YBLEGACY.constantes import *


class flfactinfo(interna):

    def __init__(self, context=None):
        super().__init__(context)

# @class_declaration sanhigia_informes #
from YBLEGACY.constantes import *
from YBUTILS.viewREST import cacheController


class sanhigia_informes(flfactinfo):

    def sanhigia_informes_esadmin(self, usuario):
        codGrupo = qsatype.FLUtil.sqlSelect(u"flusers", u"idgroup", ustr(u"iduser = '", usuario, u"' AND idgroup = 'Administracion'"))
        if codGrupo:
            return True
        else:
            return False

    def __init__(self, context=None):
        super().__init__(context)

    def esadmin(self, usuario):
        return self.iface.sanhigia_informes_esadmin(usuario)

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


form = FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
iface = form.iface
