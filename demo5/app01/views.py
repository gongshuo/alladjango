from django.shortcuts import render,redirect,HttpResponse
from .models import Administrator
# Create your views here.
# 自定义登录函数视图

def login1(request):
    message = ""
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        c = Administrator.objects.filter(username=user, password=pwd).count()
        if c:
            rep = redirect('index.html')
            rep.set_cookie('username', user)
            rep.set_cookie('password', pwd)
            return rep
        else:
            message = "用户名或密码错误"
    return render(request,'login.html', {'msg': message})


# 访问首页视图函数
def index1(request):
    # 如果用户已经登录，获取当前登录的用户名
    # 否则，返回登录页面
    username = request.COOKIES.get('username')
    password = request.COOKIES.get('password')
    c = Administrator.objects.filter(username=username, password=password).count()
    if c:
        return render(request, 'index.html', {'username': username})
    else:
        return redirect('/login.html')


def login2(request):
    message = ""
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        c = Administrator.objects.filter(username=user, password=pwd).count()
        if c:
            #加密
            rep = redirect('index.html')
            rep.set_signed_cookie('username', user)
            rep.set_signed_cookie('password', pwd)
            return rep
        else:
            message = "用户名或密码错误"
    return render(request,'login.html', {'msg': message})


def index2(request):
    # 如果用户已经登录，获取当前登录的用户名
    # 否则，返回登录页面
    username = request.get_signed_cookie('username')
    password = request.get_signed_cookie('password')
    c = Administrator.objects.filter(username=username, password=password).count()
    if c:
        return render(request, 'index.html', {'username': username})
    else:
        return redirect('/login.html')


def login(request):
    message = ""
    if request.method == "POST":
        request.session['is_login'] = True
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        c = Administrator.objects.filter(username=user, password=pwd).count()
        if c:
            request.session['is_login'] = True
            request.session['username'] = user
            rep = redirect('/index.html')
            return rep
        else:
            message = "用户名或密码错误"
    return render(request,'login.html', {'msg': message})


def auth(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get('is_login')
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/login.html')
    return inner

@auth
def index(request):
    # 如果用户已经登录，获取当前登录的用户名
    # 否则，返回登录页面
    print(666)
    username = request.session.get('username')
    c = Administrator.objects.filter(username=username).count()
    if c:
        return render(request, 'index.html', {'username': username})
    else:
        return redirect('/login.html')


def logout(request):
    request.session.clear()
    return redirect('/login.html')


from rest_framework.views import APIView
# Create your views here.


class IndexView(APIView):
    """
    สืาณ
    """
    # authentication_classes = []
    # permission_classes = []
    def get(self, request):
        # print(request)
        return HttpResponse('首页')


class IndexView2(APIView):
    """
    即使没有Token，也可以获取首页内容了
    """
    authentication_classes = []
    permission_classes = []

    def get(self,request):
        # print(request)
        return HttpResponse('首页')

