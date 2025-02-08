
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Category, SubCategory, Product, Profile, ProductDetail, ProductImage, Order, AddToCart
from django.contrib.auth.models import User
from django.db.models import Q


def homepage(request):
    categories = Category.objects.all() 
    return render(request, 'index.html', {'categories': categories, 'user': request.user})


def sub_category(request, id):
    category_instance = get_object_or_404(Category, id=id) 
    subcategories = SubCategory.objects.filter(category=category_instance) 
    return render(request, "subcategory.html", {'category': category_instance, 'subcategories': subcategories})

# def product_view(request, subcategory_id):
#     subcategory = get_object_or_404(SubCategory, id=subcategory_id)
#     products = ListPage.objects.filter(subcategory=subcategory)
#     return render(request, 'product_list.html', {'subcategory': subcategory, 'products': products})
    

# def product_detail_view(request, product_id):
#     product = get_object_or_404(ListPage, id=product_id)
#     # print(product)
#     details = product.product_details.first() 
#     is_in_cart = AddToCart.objects.filter(user=request.user, product=product).exists() if request.user.is_authenticated else False
#     return render(request, 'product_detail.html', {'product': product, 'details': details, 'is_in_cart': is_in_cart})


def view_cart(request):
    if request.user.is_authenticated:
        cart_items = AddToCart.objects.filter(user=request.user) 
        return render(request, 'cart.html', {'cart_items': cart_items})
    
def search_bar(request):
    query = request.GET.get('q', "")  

   
    # products = ListPage.objects.all()
    # categories = Category.objects.all()

    if query: 
        products = ListPage.objects.filter(
            Q(product_name__icontains=query) |
            Q(product_description__icontains=query)  
        )
        # categories = categories.filter(name__icontains=query) 

   
    return render(request, 'index.html', {
        'products': products,
        # 'categories': categories,
        'query': query
    })


def Create_category(request):
    if request.method == "POST":
        cat_name = request.POST.get("cat_name")
        cat_image = request.FILES.get("cat_image")

        
        category_instance = Category.objects.create( 
            name=cat_name,
            image=cat_image,
            user=request.user
        )
        category_instance.save()
        return redirect("homepage")
    
    return render(request, "create_category.html")


def Edit_cat(request, id):
    category_instance = get_object_or_404(Category, id=id) 

    if request.method == "POST":
        category_instance.name = request.POST['cat_name']
        
        if "cat_image" in request.FILES:
            category_instance.image = request.FILES['cat_image']

        category_instance.save()
        return redirect('homepage')

    return render(request, 'edit_cat.html', {'category': category_instance})


def create_subcategory(request, id):
    category_instance = Category.objects.get(id=id) 

    if request.method == "POST":
        category_name = request.POST.get("category_name")
        category_image = request.FILES.get("category_image")

        sub_category_instance = SubCategory.objects.create( 
            category=category_instance, 
            name=category_name, 
            image=category_image,
            user=request.user 
        )
        sub_category_instance.save()
        return redirect('homepage')    
    
    return render(request, 'create_sub_category.html', {'category': category_instance})



def edit_sub_cat(request, subcategory_id):
   
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)

    if request.method == 'POST':
        
        subcategory.name = request.POST.get('name')
        category_id = request.POST.get('category')
        if category_id:
           
            category = get_object_or_404(Category, id=category_id)
            subcategory.category = category

        if 'image' in request.FILES:
            subcategory.image = request.FILES['image']

        if 'delete_image' in request.POST and subcategory.image:
            subcategory.image.delete()

        subcategory.save()
        return redirect("homepage")
    categories = Category.objects.all()

    return render(request, 'edit_sub_category.html', {
        'subcategory': subcategory,
        'categories': categories
    })

def create_list_page(request, subcategory_id):
   
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    category = subcategory.category  

    if request.method == 'POST':
       
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        stock = request.POST.get('stock')
        product_image = request.FILES.get('product_image')

      
        list_page = ListPage.objects.create(
            product_name=product_name,
            product_price=product_price,
            stock = stock,
            product_image=product_image,
            category=category,
            subcategory=subcategory,
            user=request.user 
        )
        list_page.save()

       
        return redirect('product_view', subcategory_id=subcategory.id)  

    return render(request, 'create_list_page.html', {'subcategory': subcategory, 'category': category})

def edit_list_page(request,list_page_id):

    list_page = get_object_or_404(ListPage, id=list_page_id)
    subcategory = list_page.subcategory
    category = list_page.category

    if request.method == 'POST':
        
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        stock = request.POST.get('stock')
        product_image = request.FILES.get('product_image')

        list_page.product_name = product_name
        list_page.product_price = product_price
        list_page.stock = stock

        if product_image:
            list_page.product_image = product_image

        list_page.save()

        return redirect('product_view', subcategory_id=subcategory.id)
    return render(request, 'edit_list_page.html', {'list_page': list_page, 'subcategory': subcategory, 'category': category}) 


def create_product_detail(request, list_page_id):
    list_page = get_object_or_404(ListPage, id=list_page_id)

    if request.method == 'POST':
        product_description = request.POST['product_description']
        material = request.POST['material']
        size = request.POST['size']
        color = request.POST['color']
        additional_info = request.POST['additional_info']
        product_images = request.FILES.getlist('image')  

        
        product_detail = ProductDetail.objects.create(
            product_description=product_description,
            material=material,
            size=size,
            color=color,
            additional_info=additional_info,
            list_page=list_page 
        )

      
        for img in product_images:
            ProductImage.objects.create(product_detail=product_detail, image=img)

        return redirect('product_detail_view', product_id=product_detail.id)

    return render(request, 'create_product_detail.html', {'list_page': list_page})

def edit_product_detail(request, product_detail_id):
    product_detail = get_object_or_404(ProductDetail, id=product_detail_id)

    if request.method == 'POST':
       
        product_description = request.POST['product_description']
        material = request.POST['material']
        size = request.POST['size']
        color = request.POST['color']
        additional_info = request.POST['additional_info']
        product_image = request.FILES.getlist('image') 
        
       
        product_detail.product_description = product_description
        product_detail.material = material
        product_detail.size = size
        product_detail.color = color
        product_detail.additional_info = additional_info
        product_detail.save()

       
        delete_image_ids = request.POST.getlist('delete_images')
        for img_id in delete_image_ids:
            try:
                image_to_delete = ProductImage.objects.get(id=img_id, product_detail=product_detail)
                image_to_delete.delete()  
            except ProductImage.DoesNotExist:
                pass 

       
        for img in product_detail.images.all():
           
            new_image = request.FILES.get(f'new_image_{img.id}')
            if new_image:
                img.image = new_image 
                img.save()  

       
        for img in product_image:
            ProductImage.objects.create(product_detail=product_detail, image=img)

        return redirect('product_detail_view', product_id=product_detail.list_page.id)

    return render(request, 'edit_product_detail.html', {'product_detail': product_detail})

def add_to_cart(request,product_id):
    product = ListPage.objects.get(id=product_id)

    if not request.user.is_authenticated:
        return redirect('userlogin') 

    cart_item, created = AddToCart.objects.get_or_create(
        user=request.user, 
        product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def remove_from_cart(request, product_id):

    if not request.user.is_authenticated:
        return redirect('userlogin')
    
    cart_item = AddToCart.objects.filter(user=request.user, product_id=product_id).first()
    # if cart_item:
    cart_item.delete()
    return redirect('cart')

def create_order(request):
    if request.method == 'POST':
        shipping_address = request.POST["shipping_address"]

        cart_items = AddToCart.objects.filter(user=request.user)
        if not cart_items:
            return HttpResponse('your cart is empty')
        
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                price=item.product.product_price,
                shipping_address=shipping_address
            )
        cart_items.delete()
        return redirect('order_confirm.html')    


def createuser(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST["password"]
        email = request.POST["email"]
        phone_no = request.POST["phone_no"]
        is_vendor = request.POST["is_vendor"]

        if User.objects.filter(username=username).exists():
            return HttpResponse("User already exists.")
    
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.save()

        profile_instance = Profile.objects.create(  
            phone_no=phone_no,
            is_vendor=is_vendor,
            user=user
        )
        profile_instance.save()

        return redirect('homepage') 
    
    return render(request, "createuser.html")



def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
          
            return render(request, "userlogin.html")

    return render(request, "userlogin.html")


def userlogout(request):
    logout(request)
    return redirect('homepage')


def createuser(request):
    if request.method == "POST":

        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        email = request.POST['email']
        phone_no = request.POST['phone_number']
        is_vendor = request.POST['is_vendor' ]
        # profile_img = request.FILES['image']

        if User.objects.filter(username=username).exists():
            return HttpResponse("Error: Username already exists. Please enter another username.")
        
    

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(
            phone_no = phone_no,
            is_vendor = is_vendor,
            # image = profile_img,
            user = user

        )
        profile.save()

       
        return redirect('userlogin')
    return render(request, "createuser.html")


def get_profile(request):
    if request.user.is_authenticated:
        try:
            profile_instance = request.user.profile
            is_vendor = profile_instance.is_vendor
        except Profile.DoesNotExist:
            is_vendor = False

        return render(request, "profile.html",{'user': request.user,'is_vendor':is_vendor})
    else:
        return redirect('userlogin')        
# def get_profile(request):
#     # print(f"Is vendor: {request.user.profile.is_vendor}")
#     return render(request,'profile.html',{'user':request.user})
