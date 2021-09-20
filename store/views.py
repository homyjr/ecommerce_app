import re
from django.http import request,Http404
from django.http.response import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import *
from .utils import Cart ,dotdict
import uuid
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomerForm, PaymentForm, ShippingForm, ReviewForm
from django.core import serializers
from .storelogger import *
from django.core.paginator import Paginator
# Create your views here.

def products_display(request, **kwargs):
    """to display products on main page"""
    try:
        if 'id' in kwargs:
            category = Categories.objects.get(id = kwargs['id'])
            products = category.product.all()
            nopages = True # pagination is not applied
        else:
            allproducts = Product.objects.all()
            paginator = Paginator(allproducts, 12)
            page_number = request.GET.get('page')
            products = paginator.get_page(page_number)
            nopages = False
            
        context = {'products': products, 'nopages': nopages}
        return render(request, 'store/main.html', context)
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')



def add_to_cart(request):
    """ add items to cart """
    try:
        if request.method == 'GET':
            product_id = request.GET.get('product_id')
            product = Product.objects.get(id = product_id)
            if request.user.is_authenticated:
                customer,created = Customer.objects.get_or_create(user = request.user)
                order , created= Order.objects.get_or_create(customer = customer, is_complete = 'NO')
                
                item , item_created= order.orderitem_set.get_or_create(order = order, product = product)
                if item_created:
                    item.quantity = 1
                    item.save() 
                
                return JsonResponse({'status':True}, status=200)
            else:
                mycart = Cart(request)
                mycart.add_to_cart(product)
                return JsonResponse({'status': True}, status=200)
        else:
            JsonResponse({'status': False}, status=400)       
   
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')


def cart(request):
    """ cart page contains added items """
    try:
        if request.user.is_authenticated:
            items = Orderitem.objects.all()
            customer,created = Customer.objects.get_or_create(user = request.user)
            order , created= Order.objects.get_or_create(customer = customer, is_complete = 'NO')
            items = order.orderitem_set.all()
            total_price = order.get_total_price

            
        else:
            mycart = Cart(request)
            items = []
            cart_items = mycart.get_items
            for id, values in cart_items.items():
                item = dotdict({'product' : Product.objects.get(id = int(id)), 'get_total' : int(values['quantity'])*float(values['price']), 'quantity':values['quantity']})
                items.append(item)
            total_price= mycart.total_price  
            print(items)

        context = {'items':items,
                    'totalprice': total_price}
        return render(request, 'store/cart.html', context)

    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')




def updatecart(request):
    """ this function used to add remove or delete items """
    try:
        if request.method == 'GET': 
            price = 0
            quantity = 0
            total_price = 0
            
            if request.user.is_authenticated:
                product = Product.objects.get(id = request.GET.get('product_id')) 
                customer = Customer.objects.get(user = request.user)
                order = Order.objects.get(customer = customer, is_complete='NO')
                item = order.orderitem_set.get(product = product)
                action = request.GET.get("action")

                if action == 'add':
                    item.quantity +=1
                    item.save()
                elif action == 'subtract':
                    item.quantity -=1
                    item.save()
                else:
                    item.delete()
                    

                if item in Orderitem.objects.all(): 
                    if item.quantity <1:
                        item.delete()    
                        remove_it = 'True'

                
                
                if item in Orderitem.objects.all():
                    price = item.get_total 
                    quantity = item.quantity
                    total_price = order.get_total_price
            else:
                mycart = Cart(request)

                price, total_price, quantity = mycart.updatecart(request.GET.get('product_id'), request.GET.get("action"))

            return JsonResponse({'quantity':quantity, 'price': price, 'totalprice':total_price }, status =200)     
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')


def loginUser(request):
    """ login form for user login """
    try:
        page = 'login'
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                print("added")
                AddSessionToOrderItems(request)
                return redirect('displayproducts')

        return render(request, 'store/login_register.html', {'page': page})     
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')




def logoutUser(request):
    """ logout user """
    try:
        logout(request)
        return redirect('displayproducts')

    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')


def registerUser(request):
    """ register form for new user """
    try:
        page = 'register'
        form = CustomUserCreationForm()

        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()

                if user is not None:
                    login(request, user)
                    AddSessionToOrderItems(request)
                    return redirect('displayproducts')

        context = {'form': form, 'page': page}
        return render(request, 'store/login_register.html', context)    

    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')

def AddSessionToOrderItems(request):
    """ add items that are stored in sessions are now stored in database """
    try:
        if 'skey' in request.session:
            print('key present')
            mycart = Cart(request)
            cart_items = mycart.get_items
            print(cart_items)
            for i in cart_items.keys():
                if Orderitem.objects.filter(product_id = int(i)).exists():
                    
                    item = Orderitem.objects.get(product_id = int(i))  
                    item.quantity += int(cart_items[i]['quantity'])
                else:
                    customer = Customer.objects.get(user = request.user)
                    order , created= Order.objects.get_or_create(customer = customer, is_complete = 'NO')
                    item , item_created= Orderitem.objects.get_or_create(order = order, product_id = int(i)) 
                    item.quantity = int(cart_items[i]['quantity'])
                    
                item.save()
        else:
            print('skey not there')   

    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')          


@login_required(redirect_field_name='login')
def shippingaddress(request):
    """ shipping address form"""
    try:
        customer = Customer.objects.get(user = request.user)
        order = Order.objects.get(customer=customer,  is_complete = 'NO')
        address = Shippingaddress.objects.filter(order= order)
        if address.exists():
            address.delete()
        form = ShippingForm()
        if request.method == 'POST':
            form = ShippingForm(request.POST)
            if form.is_valid():
                sform = form.save(commit=False)
                sform.customer = customer
                sform.order = order
                sform.save()
                return redirect('payment')
    
            
        context = {
            'form': form
        }    
        
        return render(request, 'store/shipping.html', context)
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')


@login_required(redirect_field_name='login')
def payment(request):
    """ payment form"""
    try:
        if Order.objects.filter(is_complete = 'NO').exists():
            customer = Customer.objects.get(user = request.user)
            order = Order.objects.get(customer=customer,  is_complete = 'NO')
            form = PaymentForm()
            if request.method == 'POST':
                form = PaymentForm(request.POST)
                if form.is_valid():
                    pform = form.save(commit = False)
                    print("fsdsdfsfdsdg")
                    pform.order = order
                    pform.save()
                    processorder(request)
                    print("payment done")
                    return redirect('ordersuccess', id = order.transaction_id)
                else: 
                    return HttpResponse('payment error')
            else:        
                context = {
                    'form': form
                }  

                return render(request, 'store/payment.html', context)
        else:
            return HttpResponse('payment already done')
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')        

def processorder(request):
    """ after successfull payment initiate order and store it in myorders"""
    try:
        customer = Customer.objects.get(user = request.user)
        order = Order.objects.get(customer=customer,  is_complete = 'NO')
        shippingaddress = Shippingaddress.objects.get(order=order)
        order.is_complete = 'YES'
        order.save()

        myorder = Myorder.objects.get_or_create(customer = customer ,order = order, shippingaddress = shippingaddress)
        myorder[0].save()
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')    

     

@login_required(redirect_field_name='login')
def myorder(request):
    """ contains ordered items"""
    try:
        customer, created = Customer.objects.get_or_create(user = request.user)
        myorders = Myorder.objects.filter(customer = customer)
       

        context = {
            'myorders':myorders
        }

        return render(request, 'store/myorders.html', context)
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')    
    
   
def ordersuccess(request, id):
    """ order placement success page """
    try:
        context = {'transactionid': id}
        return render(request, 'store/ordersuccess.html', context)
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')


@login_required(redirect_field_name='login')
def cancelorder(request, id):
    """ cancel order in myorders"""
    try:
        myorder = Myorder.objects.get(id = id)
        myorder.delete()
        return redirect('myorder')
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')    


def search(request):
    """ search for a product"""
    try:
        if request.method == 'GET': 
            search_query = request.GET.get('search_box')
            print(search_query)
            products = Product.objects.filter(Q(name__icontains=search_query))
            context = {'products': products}
        
        return render(request, 'store/main.html', context)
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')


def ShowProductDetailsAndReviews(request , **kwargs):
    """ product page """
    try:
        reviewform = ReviewForm()
        product = Product.objects.get(id= kwargs['id'])
        reviews = product.review_set.all()[0:3]
        context = {'product':product,
                    'reviews': reviews,
                    'form':reviewform}
        return render(request, 'store/product.html', context)       
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')      

@login_required(redirect_field_name='login')
def buynow(request, **kwargs):

    try:
        product = Product.objects.get(id=kwargs['id'])
        customer ,created= Customer.objects.get_or_create(user = request.user)
        order,created = Order.objects.get_or_create(customer = customer , is_complete = 'NO')
        if order.orderitem_set.filter(product = product).exists():
            return redirect('cart')
        else:
            item , item_created= order.orderitem_set.get_or_create(order = order, product = product)
            if item_created:
                item.quantity = 1
                item.save() 
            return redirect('cart')   
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')         

            
@login_required(redirect_field_name='login')
def writereview(request):
    """ write a review"""
    try:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            product = Product.objects.get(id = request.POST.get('id'))
            customer, created = Customer.objects.get_or_create(user = request.user)
            print(form.is_valid())
            if form.is_valid():
                
                rform = form.save(commit=False)
                rform.product = product
                rform.customer = customer
                rform.save()
            return redirect('productdetails', id=request.POST.get('id')) 
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')          

def IncreaseReviews(request):
    """ when load more button is clicked load more reviews"""
    try:
        if request.method == 'GET':
            product = Product.objects.get(id = request.GET.get('id'))
            reviews = Review.objects.filter(product = product)
            review_count = int(request.GET.get('reviewcount'))
            if review_count-3 < int(reviews.count()) :
                required_reviews = reviews[review_count-3: review_count]
            else:
                required_reviews = []
            # data = serializers.serialize('json', required_reviews)
            data = []
            for i in required_reviews:
                review = i.as_dict()
                data.append(review)
            
            return JsonResponse({'reviews':data}, status=200)   
    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')         

          
@login_required(redirect_field_name='login')
def myaccount(request):
    """ user profile """
    try:
        customer = Customer.objects.get(user = request.user)
        if request.method == 'POST':
            form = CustomerForm(request.POST)
            if form.is_valid():
                customer.name = form.cleaned_data['name']
                customer.email = form.cleaned_data['email']
                customer.save()
        form = CustomerForm()   
        customerdetails = Customer.objects.get(user = request.user)
        context = {
            'form':form,
            'customerdetails':customerdetails
        }

        return render(request, 'store/myaccount.html',  context)

    except Exception as e:
        logger.error(e)
        raise Http404('Sorry some error occured')