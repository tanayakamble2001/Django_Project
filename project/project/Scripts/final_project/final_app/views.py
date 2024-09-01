from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .models import Product,Cart,Category
from django.contrib.auth.models import User



# Create your views here.
def home(request):
    return render(request,'home.html')

def register_view(request):
    if request.method == 'POST':
        f=UserCreationForm(request.POST)
        f.save()
        return redirect('/')
    else:
        f=UserCreationForm
        context={'form':f}
        return render(request,'register.html',context)
    
def login_view(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        passw=request.POST.get('password')
        user=authenticate(request,username=uname,password=passw)
        if user is not None:
            request.session['uid']=user.id
            login(request,user)
            return redirect('/')
        else:
            return render(request,'login.html')
        
    else:
        return render(request,'login.html')
    
def logout_view(request):
    logout(request)
    return redirect('/')

def product_view(request):
    #pl=Product.objects.all()
    #context={'pl':pl}
    #return render(request,'product.html',context)
    cate=Category.objects.all()
    pl=Product.objects.all()
    context={'Cate':cate,'pl':pl}
    return render(request,'product.html',context)
    
    
def add_to_cart(request,pid):
    product_id = Product.objects.get(id=pid)
    uid = request.session.get('uid')
    user_id = User.objects.get(id=uid)
    c = Cart()
    c.product=product_id
    c.user=user_id
    c.save()
    return redirect('/product')

def cartlist_view(request):
    uid = request.session.get('uid')
    cl = Cart.objects.filter(user=uid)
    context = {'cl':cl}
    return render(request,'cartlist.html',context)

def remove_view(request,pro):
    remo=Cart.objects.get(id=pro)
    remo.delete()
    return redirect('/clist')

    

def prod_search_view(request):
    uid=request.session.get('uid')
    srch=request.POST.get('srch')
    pl=Product.objects.filter(p_name__contains=srch)
    context={'pl':pl}
    return render(request,'product.html',context)

def category_page(request,category_name):
    #fname=request.session.get('fname',None)
    cate=Category.objects.all()
    pl=Product.objects.all()
    filtered_product=Product.objects.filter(category_name=category_name)
    context={'Cate':cate,'f_product':filtered_product,'pl':pl}
    return render(request,'product.html',context)

def filter_cate(request,pid):
    # cateid=Category.objects.get(id=pid)
    
    product=Product.objects.filter(category_id=pid)
    cate=Category.objects.all()
    pl=Product.objects.all()
    context={'Cate':cate,'product':product,'pl':pl}
    return render(request,'cat.html',context)

def sidebar(request):
    cate=Category.objects.all()
    context={'Cate':cate}
    return render(request,'category_list.html',context)

