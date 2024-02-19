
from django.urls import path
from accounts.views import login_page
from accounts.views import register_page
from accounts.views import activate_email
from accounts.views import cart
from accounts.views import add_to_cart
from accounts.views import remove_coupon
from accounts.views import remove_cart, checkout_cart, logoutUser


urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('activate/<email_token>/', activate_email, name='activate_email'),
    path('cart/', cart, name="cart"),
    path('add_to_cart/<uid>/', add_to_cart, name="add_to_cart"),
    path('remove-coupon/<cart_id>/', remove_coupon, name="remove_coupon"),
    path('remove-cart/<cart_item_uid>/', remove_cart, name="remove_cart"),
    path('checkout/<cart_item_uid>/', checkout_cart, name="checkout"),
    path('logout/', logoutUser, name="logout"),

]
