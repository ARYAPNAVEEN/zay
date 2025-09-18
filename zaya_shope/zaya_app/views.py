from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from .models import Products
from .models import Category
from .models import CartItem
from .models import Cart
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from admin_app.models import Category ,Discount
from .models import Order
from .models import OrderItems
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from zaya_app.models import Order



# Create your views here.
@never_cache
def index(request):
    products = Products.objects.all()

    return render(request,'user/index.html',locals())


def about(request):
    return render(request,'user/about.html')


def contact(request):
    return render(request,'user/contact.html')


def product_details(request, id):
    product = Products.objects.get(id=id)
    return render(request, 'user/shop_single.html', {'product': product})


def shop(request):
    products = Products.objects.all()
    return  render(request,'user/shop.html',locals())


def get_category(request):
    categ = Category.objects.all()
    return redirect('get_category')

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        print(password,name,email)
        exist_user =User.objects.filter(Q(email=email)|Q(phone=phone))
        if not exist_user:
            user = User.objects.create(username=name,email=email,phone=phone)
            user.set_password(password)
            user.save()
            return redirect('index')
        # else:
        #     messages.error(request,"user already exist")
        #     return redirect('index')
    return render(request,'user/index.html')
@never_cache
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email,password)

        user = authenticate(request,email=email,password=password)
        print(user)
        if user is not None:
            if user.is_superuser:
                print(user)
                login(request,user)
                print("loggedin")
                return redirect('dashboard')
            else:
                print("hdfdf")
                login(request,user)
                messages.error(request,"loin successull!")
                return redirect('index')
        else:
            messages.error(request,"invalid email and password")
    return  render(request,'user/index.html')


def logout_user(request):
    logout(request)
    return redirect('index')

def get_productdetails(request,id):
    product=Products.objects.get(id=id)
    related_products = Products.objects.filter(category=product.category)
    print(related_products)
    print(product.category)
    print(product)
    
    return render(request, 'user/shop_single.html', {'product': product, 'related_products': related_products,})
   
def get_categ(request,id):
    categ=Category.objects.get(id=id)
    print(categ.name)
    return render(request, 'admin/category.html',locals())

def cart(request):
    try:
        cart=Cart.objects.get(user=request.user)
        cart_items=CartItem.objects.filter(cart=cart)
    except:
        pass
    return render(request,'user/cart.html',locals())

def addto_cart(request,id):
    product=Products.objects.get(id=id)
    print(product)
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart=Cart.objects.create(user=request.user)
    print(cart)
    try:
        cart_item=CartItem.objects.get(cart=cart,product=product)
        cart_item.qnty += 1
        cart_item.subtotal = cart_item.qnty * product.price
        cart_item.save()
        cart.total=product.price +cart.total
        cart.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(product=product,cart=cart)
        cart_item.subtotal=cart_item.qnty*product.price
        cart_item.save()
        cart.total=cart_item.subtotal +cart.total
        cart.save()
    return redirect('cart')

def remove_cart(request,id):
    cart_item=CartItem.objects.get(id=id)
    product=cart_item.product
    cart= Cart.objects.get(user=request.user)

    if cart_item.qnty > 1:
        cart_item.qnty -= 1
        cart_item.subtotal = cart_item.qnty * product.price
        cart_item.save()
        cart.total -= product.price
        
    else:
        
        cart.total -= cart_item.subtotal
        cart_item.delete()
    cart.save()   
    return redirect('cart')
@require_POST
def update_qnty(request,id):
    cart_item=CartItem.objects.get(id=id)
    cart=cart_item.cart
    product=cart_item.product
    action = request.POST.get("action")
    if action == "increment":
        cart_item.qnty += 1
        cart_item.subtotal = cart_item.qnty * product.price
        cart.total += product.price   
        cart_item.save()

    elif action == "decrement":
        if cart_item.qnty > 1:
            cart_item.qnty -= 1
            cart_item.subtotal = cart_item.qnty * product.price
            cart.total -= product.price   
            cart_item.save()
        else:
            cart.total -= cart_item.subtotal
            cart_item.delete()
    cart.save()
    return redirect("cart")
            

        #    checkout
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if request.method == "POST":
        main_address = request.POST.get("main_address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        phone = request.POST.get("phone")

        address = Address.objects.create(
            user=request.user,
            main_address=main_address,
            city=city,
            state=state,
            pincode=pincode,
            phone=phone
        )
        order = Order.objects.create(
            user=request.user,
            address=address,
            payment_method="Pending",
            status="Pending",
            total=cart.total
        )
        
    return render(request, "user/checkout.html", locals())
        
    # need_address = not (request.user.address and request.user.phone)

    # if request.method == "POST":
    #     address = request.POST.get("address")
    #     phone = request.POST.get("phone")
    #     payment = request.POST.get("payment", "COD")

    #     # Save details if missing
    #     if need_address:
    #         request.user.address = address
    #         request.user.phone = phone
    #         request.user.save()

    #     #  Order doesn’t store address/phone, it uses user profile
    #     order = Order.objects.create(
    #         user=request.user,
    #         total=cart.total,
    #         payment_status="Pending",
    #         status="Pending",
    #     )

    #     order = Order.objects.create(
    #         user=request.user,
    #         total=cart.total,
    #         address=address,
    #         payment_method=payment_method,
    #     )

        
    #     for item in cart_items:
    #         OrderItems.objects.create(
    #             order=order,
    #             product=item.product,
    #             qnty=item.qnty,
    #             price=item.product.price,
    #         )

        
    #     cart_items.delete()
    #     cart.total = 0
    #     cart.save()

    #     return redirect("order_success" )

    # return render(request, "user/checkout.html", locals())

def order_success(request):
    return render(request, "user/order_success.html")








