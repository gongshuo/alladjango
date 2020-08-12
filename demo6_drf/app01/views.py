from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import *
# Create your views here.
from .utils.auth import Authtication

def md5(user):
    import hashlib
    import time
    ctime=str(time.time())
    m=hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    """
    登录
    """
    def post(self,request):
        ret={'code':1000,'msg':'登录成功！'}
        try:
            user=request._request.POST.get('username')
            pwd=request._request.POST.get('password')
            obj=UserInfo.objects.filter(username=user,password=pwd).first()
            if not obj:
                ret['code']=1001
                ret['msg']='用户名或密码错误'
                return JsonResponse(ret)
            #为登录用户创建token
            token=md5(user)
            #存在则更新，不存在的创建
            UserToken.objects.update_or_create(user=obj,defaults={'token':token})
            ret['token']=token

        except Exception as e:
            ret['code']=1002
            ret['msg']='请求异常'
        return JsonResponse(ret)

from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
#引入所有数据表
from .models import *
# 引入所有序列化类
from .serializers import *
#引入drf相关模块
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer
from rest_framework import exceptions
# Create your views here.


class Authtication(object):
    def authenticate(self,request):
        # 验证是否已经登录,函数名必须为：authenticate
        token = request._request.GET.get('token')
        token_obj=UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败。')
        #在rest_framework内部会将以下两个元素赋值到request，以供后续使用
        return (token_obj.user,token_obj)
    def authenticate_header(self,request):
        #这个函数可以没内容，但是必须要有
        pass


class CommonVideoView(APIView):
    """
    登录后即可访问的内容资源
    """
    renderer_classes = [JSONRenderer]  # 渲染器
    authentication_classes = [Authtication,]
    def get(self,request):
        # print(request.user,request.auth)#user1 user1
        video_list = CommonVideo.objects.all()
        re = CommonVideoSerializer(video_list, many=True)
        return Response(re.data)
#…………

#……
from .utils.auth import VIP,SVIP
# Create your views here.
#……
class VIPVideoView(APIView):
    """
    vip可访问的资源
    """
    renderer_classes = [JSONRenderer]  # 渲染器
    permission_classes = [VIP]
    def get(self,request):
        video_list = VIPVideo.objects.all()
        re = VIPVideoSerializer(video_list, many=True)
        return Response(re.data)
class SVIPVideoView(APIView):
    """
    vip可访问的资源
    """
    renderer_classes = [JSONRenderer]  # 渲染器
    permission_classes = [SVIP]
    def get(self,request):
        video_list = SVIPVideo.objects.all()
        re = SVIPVideoSerializer(video_list, many=True)
        return Response(re.data)
