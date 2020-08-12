from .serializers import BookSerializer
from .models import UserProfile, Book
from .serializers import BookModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class BookAPIView1(APIView):
    """
    第一种方式，使用Serializer
    """
    def get(self, request, format=None):
        APIKey = self.request.query_params.get("apikey", 0)
        # APIKey = request.GET['apikey']  # 同上
        developer = UserProfile.objects.filter(APIkey=APIKey).first()
        if developer:
            balance = developer.money
            if balance > 0:
                isbn = self.request.query_params.get("isbn", 0)
                books = Book.objects.filter(isbn=int(isbn))
                # books = Book.objects.all()  #获取全部
                books_serializer = BookSerializer(books, many=True)
                developer.money -= 1
                developer.save()
                return Response(books_serializer.data)
            else:
                return Response("兄弟，又到了需要充钱的时候！好开心啊！")
        else:
            return Response("查无此人啊")


class BookAPIView2(APIView):
    """
    第二种方式，使用ModelSerializer
    """
    def get(self, request, format=None):
        APIKey = self.request.query_params.get("apikey", 0)
        developer = UserProfile.objects.filter(APIkey=APIKey).first()
        # APIKey = request.GET['apikey']  # 同上
        if developer:
            balance = developer.money
            if balance > 0:
                isbn = self.request.query_params.get("isbn", 0)
                books = Book.objects.filter(isbn=int(isbn))
                books_serializer = BookModelSerializer(books, many=True)   # 区别
                developer.money -= 1
                developer.save()
                return Response(books_serializer.data)
            else:
                return Response("兄弟，又到了需要充钱的时候！好开心啊！")
        else:
            return Response("查无此人啊")


from rest_framework import mixins
from rest_framework import generics


class BookMixinView1(mixins.ListModelMixin, generics.GenericAPIView):
    """
    第三种方式
    """
    # 使用mixins.ListModelMixin + generics.GenericAPIView对APIView进行一次封装，至少需要加一个get函数：
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer

    def get(self, request, *args, **kwargs):       # 如果这里不加get函数，代表默认不支持get访问这个api，所以必须加上
        APIKey = self.request.query_params.get("apikey", 0)
        # APIKey = request.GET['apikey']  # 同上
        developer = UserProfile.objects.filter(APIkey=APIKey).first()
        if developer:
            balance = developer.money
            if balance > 0:
                isbn = self.request.query_params.get("isbn", 0)
                developer.money -= 1
                developer.save()
                self.queryset = Book.objects.filter(isbn=int(isbn))
                return self.list(request, *args, **kwargs)
            else:
                return Response("兄弟，又到了需要充钱的时候！好开心啊！")
        else:
            return Response("查无此人啊")


class BookMixinView2(generics.ListAPIView):
    """
    第四种方式
    """
    # 使用generics.ListAPIView则可以不用加get这个函数，
    # 因为generics.ListAPIView相对于mixins.ListModelMixin+generics.GenericAPIView而言，
    # 所谓的封装，就是封装了一个get函数罢了。
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer

    def get(self, request, *args, **kwargs):
        APIKey = self.request.query_params.get("apikey", 0)
        developer = UserProfile.objects.filter(APIkey=APIKey).first()

        if developer:
            balance = developer.money
            if balance > 0:
                isbn = self.request.query_params.get("isbn", 0)
                developer.money -= 1
                developer.save()
                self.queryset = Book.objects.filter(isbn=int(isbn))
                return self.list(request, *args, **kwargs)
            else:
                return Response("兄弟，又到了需要充钱的时候！好开心啊！")
        else:
            return Response("查无此人啊")


from rest_framework import viewsets
from rest_framework.permissions import BasePermission


class IsDeveloper(BasePermission):
    message = '查无此人啊'

    def has_permission(self, request, view):
        APIKey = request.query_params.get("apikey", 0)
        developer = UserProfile.objects.filter(APIkey=APIKey).first()
        if developer:
            return True
        else:
            print(self.message)
            return False


class EnoughMoney(BasePermission):
    message = "兄弟，又到了需要充钱的时候！好开心啊！"

    def has_permission(self, request, view):
        APIKey = request.query_params.get("apikey", 0)
        developer = UserProfile.objects.filter(APIkey=APIKey).first()
        balance = developer.money
        if balance > 0:
            developer.money -= 1
            developer.save()
            return True
        else:
            print(self.message)
            return False


class BookModelViewSet(viewsets.ModelViewSet):
    """
    第五种方式
    """
    authentication_classes = []
    # Django REST framework的权限组件有一个原则，即没有认证就没有权限！
    permission_classes = [IsDeveloper, EnoughMoney]
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer

    def get_queryset(self):
        isbn = self.request.query_params.get("isbn", 0)
        books = Book.objects.filter(isbn=int(isbn))
        queryset = books
        return queryset