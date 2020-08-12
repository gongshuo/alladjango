from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.


class IndexView1(APIView):
    """
    演示视图
    """
    def get(self,request):
        return render(request,'index.html')


class IndexView(APIView):
    """
    演示视图
    """
    def get(self,request):
        j=0
        for i in request.META:
            print(i,":",request.META[i])
            j+=1
        print("共",j,"条信息")
        return render(request,'index.html')


from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
# Create your views here.


class IndexView(APIView):
    """
    演示视图
    """
    throttle_classes = (AnonRateThrottle,)

    def get(self,request):
        return Response('本网页代表了所有浏览量高能带来收益的网页。')