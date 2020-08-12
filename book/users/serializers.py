from rest_framework import serializers

from .models import UserProfile, Book


# 第一种序列方式
class BookSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=100)
    isbn = serializers.CharField(required=True, max_length=100)
    author = serializers.CharField(required=True, max_length=100)
    publish = serializers.CharField(required=True, max_length=100)
    rate = serializers.FloatField(default=0)


# 第二种序列方式
class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"           # 将整个表的所有字段都序列化
        # fields = ('title', 'isbn', 'author')  # 指定序列化某些字段

