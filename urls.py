from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.view_cart, name='view_cart'), 
    path('my-orders/', views.my_orders, name='my_orders'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('buy-cart-items/', views.buy_cart_items, name='buy_cart_items'),
]
