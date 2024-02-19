from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import Profile, Cart, CartItem
from products.models import Product, SizeVariant, Coupon


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
        user = Profile.objects.select_related(email_token=email_token).all()
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
        size_variant = SizeVariant.objects.select_related(size_name=variant)
        cart_item.size_variant = size_variant
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):

    cart_obj = Cart.objects.get(is_paid=False, user=request.user)

    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon)

        if not coupon_obj.exists():
            messages.warning(request, 'Invalid Coupon code')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.coupon:
            messages.warning(request, 'coupon already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(
                request, f'coupon minimum amount not met must be greater the {coupon_obj[0].minimum_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj[0].is_expired:
            messages.warning(request, 'coupon expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, 'coupon applied successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {'cart': cart_obj}

    return render(request, 'accounts/cart.html', context=context)


def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid=cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request, 'coupon removed successfully')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItem.objects.get(uid=cart_item_uid)
        cart_item.delete()
        messages.success(request, 'Cart item removed successfully')
    except CartItem.DoesNotExist:
        messages.error(request, 'Cart item not found')
    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
