"""
URL configuration for Trendify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
   

    # Category Views #
    path('create/', Create_category, name='Create_category'),
    path('category/edit/<int:id>/', Edit_cat, name='edit_category'),

    # Subcategory Views #
    path('sub_category/<int:id>/', sub_category, name="sub_category"), 
    path('create_subcategory/<int:id>/', create_subcategory, name="create_subcategory"), 
    path('edit_sub_cat/<int:subcategory_id>/', edit_sub_cat, name="edit_sub_category"), 
    
   
    ## product_page ##
    path('products_list_page/<int:subcategory_id>/', product_list_page, name='product_list_page'),
    path('product_detail/<int:product_id>/', product_detail, name='product_detail'),
    path('create-product/<int:subcategory_id>/', create_product, name='create_product'),
    path('edit-product/<int:product_id>/', Edit_product_page, name='edit_product'),
       
   
   ## cart options ##
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),

    # order urls
    path('order/', proceed_order, name="proceed_order"),
    path('order/cancel/<int:order_id>/', cancel_order, name='cancel_order'),
    path('history/', order_history, name="order_history"),
    path('mark_as_delivered/<int:order_id>/', mark_as_delivered, name='mark_as_delivered'),
    path('search/', search_bar, name="search_bar"),

   
    # User authentication Views #
    path('create_user/', createuser, name='create_user'),
    path('login/', userlogin, name="userlogin"),
    path('logout/', userlogout, name="userlogout"),
    path('profile/', get_profile, name='get_profile'),
    

] + static(settings.STATIC_URL, documents_root= settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   