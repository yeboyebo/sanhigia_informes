# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration sanhigia #
from django.shortcuts import render
from django.http import HttpResponseRedirect
from YBUTILS.viewREST import cacheController, accessControl
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth
from django.contrib.auth.models import User, Group
import hashlib

from models.flfactppal.usuarios import usuarios
from models.flfactppal.agentes import agentes


class sanhigia(interna):

    def sanhigia_login(self, request, error=None):
        """ Peticion defecto"""
        if not error:
            error = ''
        return render(request, 'portal/login.html', {'error': error})

    def sanhigia_auth_login(self, request):

        _i = self.iface

        if request.method == 'POST':
            action = request.POST.get('action', None)
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)

            if action == 'login':
                if username == "admin":
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login_auth(request, user)
                        accessControl.accessControl.registraAC()
                    else:
                        return _i.login(request, 'Error de autentificación')
                    return HttpResponseRedirect("/")
                try:
                    sisuser = User.objects.get(username=username)
                except Exception as e:
                    # Si no existe usuario en django lo creamos(Si existe el usuario en tabla usuarios)
                    try:
                        usuario = usuarios.objects.filter(idusuario__exact=username)
                        if len(usuario) == 0:
                            return _i.login(request, 'No existe el usuario')
                        user = User.objects.create_user(username=username, password="Sh20Pda17")
                        user.is_staff = False
                        user.groups.add(Group.objects.get(name='agentes'))
                        user.save()
                    except Exception as e:
                        print(e)
                usuario = usuarios.objects.get(idusuario=username)
                md5passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
                print("falla por aqui??", usuario.password, md5passwd)
                if usuario.password != md5passwd:
                    print("si no")
                    return _i.login(request, 'Error de autentificación')
                user = authenticate(username=username, password="Sh20Pda17")
                if user is not None:
                    login_auth(request, user)
                    accessControl.accessControl.registraAC()
                else:
                    return _i.login(request, 'Error de autentificación')
                return HttpResponseRedirect("/")
        return _i.login(request)

    def sanhigia_account_request(self, request):
        return HttpResponseRedirect("/")

    def __init__(self, context=None):
        super(sanhigia, self).__init__(context)

    def auth_login(self, request):
        return self.ctx.sanhigia_auth_login(request)

    def account_request(self, request):
        return self.ctx.sanhigia_account_request(request)

    def login(self, request, error=None):
        return self.ctx.sanhigia_login(request, error)


# @class_declaration head #
class head(sanhigia):

    def __init__(self, context=None):
        super(head, self).__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super(ifaceCtx, self).__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)
