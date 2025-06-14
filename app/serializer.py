
from rest_framework import serializers
from app.models import *
from django.contrib.auth.models import User



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'is_vendor', 'phone_no']        
   
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    phone_number = serializers.CharField(source="profile.phone_no", required=False)
    is_vendor = serializers.BooleanField(source="profile.is_vendor", required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'phonen_umber', 'is_vendor']
        read_only_fields = ['id', 'username', 'email']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id','username','first_name','last_name','password','email','profile')
        read_only_fields = ('id', 'username', 'email') 


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')
        read_only = ('user',)


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        

class ProductImageSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True)
    class Meta:
        model = ProductImage
        # fields = ('id', 'product', 'image')
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'        

class AddToCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = AddToCart
        fields = ['id','user', 'product', 'quantity', 'added_at']
#         fields = ('id', 'user', 'product', 'price', 'quantity', 'booking_date', 'delivery_date', 'status', 'shipping_address', 'payment_method')

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
    # user = UserSerializer(read_only=True)
    # review_text = serializers.CharField(max_length=100)
    # rating = serializers.IntegerField()
    # product_id = serializers.IntegerField()
    # user_id = serializers.IntegerField()
    # created_at = serializers.DateTimeField()


class SubCategoryByCategory(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
 
class ProductBysubcategory(serializers.ModelSerializer):
    images=ProductImageSerializer(many=True,read_only=True)
    class Meta:
        model=Product
        fields = '__all__'
              
class ProductReviews(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        # fields = ['id', 'review_text', 'rating','user'] 
        fields = '__all__'
