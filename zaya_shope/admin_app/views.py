from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
from django.contrib.auth import authenticate,login,logout
from .models import Products
from .models import Category ,Discount

# Create your views here.

def dashboard(request):
    return render(request,'admin/dashboard.html')


def products(request):
    products = Products.objects.all()
    categorys = Category.objects.all()
    print(categorys)

    return render(request,'admin/products.html',locals())



def add_product(request):
    categorys = Category.objects.all()
    print(categorys)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category_id = request.POST.get('category')  
        print(category_id)
        discount_id= request.POST.get('discount')
        print(discount_id)
        image = request.FILES.get('image')
        stock = request.POST.get('stock')
        discount_obj = None
        discount_price = price
        if discount_id:
            try:
                discount_obj = Discount.objects.get(id=discount_id)
                discount_value = discount_obj.percentage
                discount_price = price - (price * Decimal(discount_value) / 100)
            except Discount.DoesNotExist:
                discount_obj = None 
        try:
            cat = Category.objects.get(id=category_id) 
            print(cat)
            Products.objects.create(
                name=name,
                price=price,
                discount=discount_obj,
                description=description,
                discount_price=discount_price,
                category=cat,
                image=image,
                stock=stock
            )
            
            return redirect('products')
        except Category.DoesNotExist:
            print(" Category not found")
    
    return render(request, 'admin/add_product.html', {'categorys': categorys})



def get_product(request,id):
    product=Products.objects.get(id=id)
    return redirect('update', id=id)


def edit(request, id):
    product = Products.objects.get(id=id)
    categorys = Category.objects.all()
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        category_id = request.POST.get('category')
        product.category = Category.objects.get(id=category_id)
        product.stock = request.POST.get('stock')
        print("PRODUCT CATEGORY:", product.category) 
        if 'image' in request.FILES:
            product.image = request.FILES.get('image')
        product.save()
        return redirect('products')  
    choices=categorys
    return render(request, 'admin/edit.html', locals())

def delete(request,id):
    product=Products.objects.get(id=id)
    product.delete()
    return redirect('products')



    # category
def category(request):
    categ = Category.objects.all()
    return render(request,'admin/category.html',locals())



def add_categ(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        image=request.FILES.get('image')
        print(image)
        categ=Category.objects.create(name=name,image=image)
        return redirect('category')
    return render(request,'admin/category.html',locals())



def get_categ(request,id):
    categ=Category.objects.get(id=id)
    return render(request, 'admin/category.html',locals())


def edit_categ(request,id):
    categ=Category.objects.get(id=id)
    if request.method == 'POST':
        categ.name=request.POST.get('name')
        if 'image' in request.FILES:
          categ.image=request.FILES.get('image')
        categ.save()
        return redirect('category')
    return render(request,'admin/categ_edit.html',locals())

def delete_categ(request,id):
    categ=Category.objects.get(id=id)
    categ.delete()
    return redirect('category')

