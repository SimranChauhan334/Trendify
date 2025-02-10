
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Category, SubCategory, Product, Profile,  ProductImage, Order, AddToCart
from django.contrib.auth.models import User
from django.db.models import Q


def homepage(request):
    categories = Category.objects.all() 
    return render(request, 'index.html', {'categories': categories, 'user': request.user})


def sub_category(request, id):
    category_instance = get_object_or_404(Category, id=id) 
    subcategories = SubCategory.objects.filter(category=category_instance) 
    return render(request, "subcategory.html", {'category': category_instance, 'subcategories': subcategories})

def product_list_page(request, subcategory_id):
    
    if not request.user.is_authenticated:
        return redirect('userlogin') 
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
   
    products = Product.objects.filter(subcategory=subcategory)

    return render(request, 'product_list.html', {
        'subcategory': subcategory,
        'products': products
    })


def product_detail(request, product_id):
   
    product = get_object_or_404(Product, id=product_id)
    
   
    images = product.images.first()  
    
    
    if request.user.is_authenticated:
        is_in_cart = AddToCart.objects.filter(user=request.user, product=product).exists()
    else:
        is_in_cart = False

    return render(request, 'product_detail.html', {
        'product': product,
        'images': images,
        'is_in_cart': is_in_cart  
    })

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = AddToCart.objects.filter(user=request.user) 
        
        
        for item in cart_items:
            item.product_images = item.product.images.first()  

        return render(request, 'cart.html', {'cart_items': cart_items})
    else:
        return redirect('userlogin')


def search_bar(request):

    query = request.GET.get('q','')
    products = Product.objects.all()
    categories = Category.objects.all()


    if query :
        products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(category__name__icontains=query)
        )
        categories = Category.objects.filter(name__icontains=query)
    return render(request, 'index.html', {
        'products': products,
        'categories':categories,
        'query': query,
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

def create_product(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)  # Get subcategory by ID
    category = subcategory.category  
    
    if request.method == 'POST':
       
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_description = request.POST.get('product_description')
        color = request.POST.get('color')
        material = request.POST.get('material')
        stock = request.POST.get('stock')

        product = Product(
            product_name=product_name,
            product_price=product_price,
            product_description=product_description,
            color=color,
            material=material,
            stock=stock,
            subcategory=subcategory,  
            category=category, 
        )
        product.save()
       
        images = request.FILES.getlist('images')  
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return redirect('product_list_page', subcategory_id=subcategory_id)

    return render(request, 'create_product.html', {'subcategory_id': subcategory_id, 'subcategory': subcategory})


def Edit_product_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        
        product.product_name = request.POST.get("product_name")
        product.product_price = request.POST.get("product_price")
        product.product_description = request.POST.get("product_description")
        product.color = request.POST.get("color")
        product.material = request.POST.get("material")
        product.stock = request.POST.get("stock")
        
       
        delete_images = request.POST.getlist("delete_images") 
        for image_id in delete_images:
            image = get_object_or_404(ProductImage, id=image_id)
            image.delete()

       
        for image_id in product.images.all():
            new_image = request.FILES.get(f"new_image_{image_id.id}")
            if new_image:
               
                image_id.image = new_image
                image_id.save()

       
        new_images = request.FILES.getlist("new_images")
        for new_image in new_images:
            ProductImage.objects.create(product=product, image=new_image)

        product.save()
        return redirect("product_detail", product_id=product.id)

    return render(request, 'edit_product_page.html', {'product': product})



def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    quantity = int(request.POST.get('quantity', 1)) 

    if quantity > product.stock:
        
        return HttpResponse(f"Only {product.stock} items are available.", status=400)

   
    cart_item, created = AddToCart.objects.get_or_create(user=request.user, product=product)

    if not created:
        
        cart_item.quantity += quantity
    else:
      
        cart_item.quantity = quantity
    
    # Save the cart item
    cart_item.save()
    return redirect('cart_page')  # Redirect to the cart page
# def add_to_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
   

#     if not request.user.is_authenticated:
#         return redirect('userlogin') 

#     cart_item, created = AddToCart.objects.get_or_create(
#         user=request.user, 
#         product=product)
    
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()

#     return redirect('cart')



def remove_from_cart(request, product_id):

    if not request.user.is_authenticated:
        return redirect('userlogin')
    
    cart_item = AddToCart.objects.filter(user=request.user, product_id=product_id).first()
    # if cart_item:
    cart_item.delete()
    return redirect('cart')


def create_order(request):
    if not request.user.is_authenticated:
        
        return redirect('login')  
    
    
    cart_items = AddToCart.objects.filter(user=request.user)
    
    if cart_items.exists():
       
        for item in cart_items:
            item.total_price = item.product.product_price * item.quantity 
        
        
        total_amount = sum(item.total_price for item in cart_items)

        
        return render(request, 'order.html', {'cart_items': cart_items, 'total_amount': total_amount})
    
   
    return redirect('product_list_page')



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
