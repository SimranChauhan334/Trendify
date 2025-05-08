
from rest_framework import serializers
from app.models import *
from django.contrib.auth.models import User



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'is_vendor', 'phone_no']        
   

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('username','first_name','last_name','password','email','profile')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')
        read_only = ('user',)


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    # product = ProductSerializer(read_only=True)
    class Meta:
        model = ProductImage
        # fields = ('id', 'product', 'image')
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'        

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddToCart
        fields = ['user', 'product', 'quantity', 'added_at']
#         fields = ('id', 'user', 'product', 'price', 'quantity', 'booking_date', 'delivery_date', 'status', 'shipping_address', 'payment_method')

class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

class ReviewSerializer(serializers.Serializer):

    review_text = serializers.CharField(max_length=100)
    rating = serializers.IntegerField()
    product_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class SubCategoryByCategory(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

 
class ProductBysubcategory(serializers.ModelSerializer):
    images=ProductImageSerializer(many=True,read_only=True)
    class Meta:
        model=Product
        fields = '__all__'
              
