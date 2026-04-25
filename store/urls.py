from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart_view, name='cart'),
path('increase/<int:item_id>/', views.increase_quantity, name='increase'),
path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease'),
path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]