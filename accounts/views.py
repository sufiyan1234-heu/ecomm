from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile, Cart, CartItem
from products.models import Product, SizeVariant


# Create your views here.


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)
        print(user_obj)
        print(password, email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Please verify your email.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email, password=password)
        print(user_obj)

        if user_obj:
            login(request, user_obj)
            return redirect('/')

        messages.warning(request, 'Invalid password provided ')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(email=email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(username=email,
                                       first_name=first_name,
                                       last_name=last_name,
                                       email=email,
                                       password=password)

        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')


def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Your account has been activated.')
        return redirect('/')
    except Exception as e:
        return HttpResponse('invalid email token')


def add_to_cart(request, uid):
    variant = request.GET.get('variant')
    product = Product.objects.get(uid=uid)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item = CartItem.objects.create(cart=cart, product=product)

    if variant:
        size_variant = SizeVariant.objects.get(size_name=variant)
        cart_item.size_variant = size_variant
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):
    try:
        context = {'cart': Cart.objects.get(is_paid=False, user=request.user)}
        print(context['cart'])
    except Cart.DoesNotExist:
        context = {'cart': None}

    if request.method == 'POST':
        pass

    return render(request, 'accounts/cart.html', context=context)
