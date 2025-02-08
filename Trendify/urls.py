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
from django.urls import path
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

    ## List Page ##
    path('create_list_page/<int:subcategory_id>/', create_list_page, name='create_list_page'),
    path('products/<int:subcategory_id>/', product_view, name='product_view'),
    path('edit_list_page/<int:list_page_id>/', edit_list_page, name='edit_list_page'),

    ## product_page ##
    path('create_product_detail/<int:list_page_id>/', create_product_detail, name='create_product_detail'),
    path('product/<int:product_id>/', product_detail_view, name='product_detail_view'),
    path('product/edit/<int:product_detail_id>/', edit_product_detail, name='edit_product_detail'),
   
    # path('product/<int:product_id>/', product_detail_view, name='product_detail_view'),
   
   ## cart options ##
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('order/', create_order, name="create_order"),
   
    # User authentication Views #
    path('create_user/', createuser, name='create_user'),
    path('login/', userlogin, name="userlogin"),
    path('logout/', userlogout, name="userlogout"),
    path('profile/', get_profile, name='get_profile'),
     path('search/', search_bar, name='search'),


] + static(settings.STATIC_URL, documents_root= settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   