from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import urllib.request
import math,string, random
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from .forms import CreateUserForm
from django.contrib.auth.models import Group

# Create your views here.

def home(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']

    products = Product.objects.all()
    context = {'products': products, 'order': order, 'cartItems': cartItems}
    return render(request, 'Dashboard/index.html', context)

def women(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']

    products = Product.objects.all()
    context = {'products': products, 'order': order, 'cartItems': cartItems}
    return render(request, 'Dashboard/women.html', context)

def men(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']

    products = Product.objects.all()
    context = {'products': products, 'order': order, 'cartItems': cartItems}
    return render(request, 'Dashboard/men.html', context)

def products(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']

    products = Product.objects.all()
    context = {'products': products, 'order': order, 'cartItems': cartItems}
    return render(request, 'Dashboard/products.html', context)

def account(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            recaptcha_response = request.POST.get('g-recaptcha-response')

            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY, 'response': recaptcha_response}
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())

            if result['success']:
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    # login(request, user)
                    request.session['username'] = username
                    request.session['password'] = password
                    obj = Customer.objects.get(name=username)
                    email = obj.email
                    o = generateOTP()
                    print(o)
                    htmlgen = '<p>Your OTP is </p>' + o
                    send_mail('OTP request', o, 'adorftest@gmail.com', [email], fail_silently=False,html_message=htmlgen)
                    global otp
                    def otp():
                        return o
                    return redirect('verify_otp')
                else:
                    messages.info(request, 'Username Or Password is Incorrect')
            else:
                messages.error(request,
                               'Invalid reCAPTCHA. Please try again.')



    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']

    products = Product.objects.all()
    context = {'products': products, 'order': order, 'cartItems': cartItems}

    return render(request, 'Dashboard/account.html', context)

def verify_otp(request):
    ot=otp()
    username=request.session['username']
    password=request.session['password']
    if request.method == "POST":
        otpfromback = request.POST.get('otp')
        if otpfromback == ot:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('index')
            else:
                messages.info(request, 'Session is Changed')
        else:
            messages.error(request,
                           'Enter the OTP you recieved and try again.')

    return render(request, 'Dashboard/verify_otp.html')

def accountlogout(request):
    logout(request)
    return redirect('account')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('account')

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']

    products = Product.objects.all()
    context = {'products': products, 'order': order, 'cartItems': cartItems, 'form': form}
    return render(request, 'Dashboard/register.html', context)

def contact(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']

    products = Product.objects.all()
    context = {'products': products, 'order': order, 'cartItems': cartItems}
    return render(request, 'Dashboard/contact.html',context)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'Dashboard/checkout.html', context)

def single(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']

    products = Product.objects.all()
    context = {'products': products, 'order': order, 'cartItems': cartItems}
    return render(request, 'Dashboard/single.html', context)

@login_required(login_url='account')
def address(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'Dashboard/address.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
         Payment.objects.create(
            customer=customer,
            order=order,
            cname=data['payment']['cname'],
            cardNum=data['payment']['cardNum'],
            cvv=data['payment']['cvv'],
            exd=data['payment']['exd'],
        )
         ShippingAddress.objects.create(
            customer=customer,
            order=order,
            state=data['shipping']['state'],
            city=data['shipping']['city'],
            phoneNum=data['shipping']['phoneNum'],
            pickaddress=data['shipping']['pickaddress'],
        )
         email = request.user.customer.email
         htmlgen="<p>Your Order Was Completed Successsfully</p>"
         send_mail('Order Completed', "Your Order Was Completed Successfully", 'adorftest@gmail.com', [email], fail_silently=False, html_message=htmlgen)

	return JsonResponse('Payment submitted..', safe=False)


def generateOTP():
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(4)))
    str1 += ''.join((random.choice(string.digits) for x in range(6)))
    sam_list = list(str1)  # it converts the string to list.
    random.shuffle(sam_list)  # It uses a random.shuffle() function to shuffle the string.
    OTP = ''.join(sam_list)
    return OTP


def send_otp(request):
    username = request.POST.get('username')
    obj = Customer.objects.get(name=username)
    email = obj.email
    o = generateOTP()
    print(o)
    htmlgen = '<p>Your OTP is </p>' + o
    send_mail('OTP request', o, 'adorftest@gmail.com', [email], fail_silently=False, html_message=htmlgen)
    return HttpResponse(o)

@login_required(login_url='account')
def customer_profile(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    customer = request.user.customer
    shipping = ShippingAddress.objects.filter(customer=customer)
    payment = Payment.objects.filter(customer=customer)
    orderhistory = Order.objects.filter(customer=customer)

    context = {'items': items,
               'order': order,
               'cartItems': cartItems,
               'shipping': shipping,
               'payment': payment,
               'ordered': orderhistory,}


    return render(request, 'Dashboard/customerprofile.html', context)





