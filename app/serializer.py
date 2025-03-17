
from rest_framework import serializers
from app.models import *
from django.contrib.auth.models import User




class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ('id','product_name', 'product_price')
        # fields = ('product_name','product_price')


class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    # product = ProductSerializer(read_only=True)
    class Meta:
        model = ProductImage
        fields = ('id','product','image')

class AddToCart(serializers.HyperlinkedModelSerializer):
    class Meta:
        models = AddToCart
        fields = ('id', 'user', 'product', 'price', 'quantity', 'booking_date', 'delivery_date', 'status', 'shipping_address', 'payment_method')

