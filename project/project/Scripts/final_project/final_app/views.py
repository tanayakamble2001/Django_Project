from django.conf import settings
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .models import Product,Cart,Category
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

import razorpay



# Create your views here.
def home(request):
    return render(request,'home.html')

def register_view(request):
    if request.method == 'POST':
        #f=UserCreationForm(request.POST)
        uname=request.POST.get('username')
        passw=request.POST.get('password')
        c_passw=request.POST.get('c_password')
        u=User()
        u.username=uname
        u.password=passw
        user=User.objects.filter(username=uname)
        if len(uname) > 10:
            messages.error(request, "Username must be under 10 character.")
            return redirect('/register')
        if passw != c_passw:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        if user.exists():
            messages.info(request, "Username is already taken. ")
            return redirect('/register')
        u.save()
        messages.info(request, "Account Created Successfully.")
        return redirect('/')
    else:
        return render(request,'register.html')
    
def login_view(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        passw=request.POST.get('password')
        user=authenticate(request,username=uname,password=passw)
        user1=User.objects.filter(username=uname)
        if user1.exists():
            if user is not None:
                request.session['uid']=user.id
                login(request,user)
                return redirect('/')
            else:
                return render(request,'login.html')
        else:
            messages.info(request, "You are not Register.")
            return redirect('/login')
        
        
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
    if Cart.objects.filter(user_id=uid,product=product_id).exists():
        return redirect('/product')
    c = Cart()
    c.product=product_id
    c.user=user_id
    c.save()
    return redirect('/product')

def cartlist_view(request):
    uid = request.session.get('uid')
    user_id= User.objects.get(id=uid)
    cl = Cart.objects.filter(user_id=uid)
            #Calculate total and final price
    total_price = sum((item.product.p_price)*item.quantity for item in cl)
    final_price= total_price * 100

    if final_price < 100:
        return render(request,'cartlist.html',{
            'cl': cl,
            'error' : 'Order amount is too low. Please add more items to your cart'
            })
    
        #Create payment order with Razorpay
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    payment= client.order.create({'amount': final_price,'currency': 'INR', 'payment_capture': '1'})
    print(payment)

        #Save payment order details in session or database if necessary

    request.session['razorpay_order_id'] = payment['id']

    context = {'cl':cl, 'total_price':total_price,
               'final_price': final_price, 'razorpay_key_id': settings.RAZORPAY_KEY_ID,
               'razorpay_order_id': payment['id']}
    return render(request,'cartlist.html',context)

def update_cart(request, item_id, action):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity < 1:
            cart_item.delete()
            return redirect('/clist')
        
    cart_item.save()
    return redirect('/clist')

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


@csrf_exempt

def success_view(request):
    if request.method=='POST':
        a=request.POST
        print(a)
        return render(request,'success.html')
    else:
        return render(request,'success.html')