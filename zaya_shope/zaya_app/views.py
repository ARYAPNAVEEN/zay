from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from .models import Products
from .models import Category
from .models import CartItem

from django.views.decorators.cache import never_cache
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




def get_productdetails(request,id):
    product=Products.objects.get(id=id)
    related_products = Products.objects.filter(category=product.category)
    print(related_products)
    print(product.category)
    print(product)
    print(1,2,556789876543)
    return render(request, 'user/shop_single.html', {'product': product, 'related_products': related_products})
   


def cart(request):

    return render(request,'user/cart.html')




def logout_user(request):
    logout(request)
    return redirect('index')




