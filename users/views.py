# coding: utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from users.forms import RegisterForm, LoginForm
from users.models import UserProfile


class RegisterView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return JsonResponse({'status': False, 'msg': 'Method not allowed...'})

    def post(self, request):
        register_form = RegisterForm(request.POST)  # 验证传过来的参数
        if register_form.is_valid():
            email = request.POST.get('email', '')  # 获取邮箱
            try:
                UserProfile.objects.get(email=email)  # 如果邮箱已经存在
                return JsonResponse({'status': False, 'msg': 'Email：%s already exists...' % email})
            except ObjectDoesNotExist:
                password = request.POST.get('password', '')  # 获取密码
                retype_password = request.POST.get('retype_password', '')  # 确认密码
                if password == retype_password:
                    UserProfile.objects.create(username=email, email=email, password=make_password(password))
                    # Message.objects.create(body="用户%s于%s进行了注册" % (email, timezone.localtime()))
                    return JsonResponse({'status': True, 'msg': 'User Register Success...'})
                else:
                    return JsonResponse({'status': False, 'msg': 'Passwords does not match...'})
        else:
            return JsonResponse({'status': False, 'msg': register_form.errors})


class LoginView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return JsonResponse({'status': False, 'msg': 'Method not allowed...'})

    def post(self, request):
        """验证用户是否是否可以成功登录"""
        login_form = LoginForm(request.POST)  # FORM验证传过来的值是否合法
        if login_form.is_valid():  # 验证是否错误
            email = request.POST.get('email', '')  # 获取用户名
            password = request.POST.get('password', '')  # 获取密码
            user = authenticate(username=email, password=password)  # 验证用户名和密码
            if user is not None:  # 如果用户名和密码匹配
                if user.is_active:  # 如果用户是激活状态
                    login(request, user)  # 把SESSION和COOKIE写入request
                    return JsonResponse({'status': True, 'msg': 'Login success...'})
                    # if user.is_superuser:
                    #     return HttpResponseRedirect(reverse('admin:dashboard'))  # 返回首页
                    # else:
                    #     return HttpResponseRedirect(reverse('index'))  # 返回首页
                else:  # 用户未激活
                    return JsonResponse({'status': False, 'msg': 'User not activated...'})
            else:  # 用户名和密码错误
                return JsonResponse({'status': False, 'msg': 'Wrong username or password...'})
        else:  # FORM验证出错，并吧出错信息传递到前端
            return JsonResponse({'status': False, 'msg': login_form.errors})


class LogoutView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        return JsonResponse({'status': True, 'msg': 'Logout success...'})
