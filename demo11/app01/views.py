from django.shortcuts import render
from django.views.generic.base import View
from .models import Books
# Create your views here.
class BookListView(View):
    """
    获取图书列表
    """
    def get(self,request):
        list=Books.objects.all()
        return render(request,'booklist.html',{'list':list})

class GetBookView1(View):
    """
    获取单个图书
    """
    def get(self,request,id):
        book=Books.objects.filter(id=id).first()
        print(book.pv)
        book.pv+=1
        book.save()
        return render(request,'book.html',{'t':book})

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
class GetBookView(View):
    """
    获取单个图书
    """
    @method_decorator(cache_page(3))
    def get(self,request,id):
        book=Books.objects.filter(id=id).first()
        print(book.pv)
        book.pv+=1
        book.save()
        return render(request,'book.html',{'t':book})

from django.shortcuts import render
from .models import Goods
from .serializers import GoodsModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
# Create your views here.
class GetGoodListView(APIView):
    """
    获取商品列表
    """
    def get(self,request):
        good_list=Goods.objects.all()
        re=GoodsModelSerializer(good_list,many=True)
        return Response(re.data)

