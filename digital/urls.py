from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category_detail'),
    path('add_favourite/<slug:product_slug>/', save_favorite_product, name='add_favourite'),
    path('my_favourite/', FavouriteProductsView.as_view(), name='favourite_products'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', register, name='register'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('chg_profile_view/', chg_profile_view, name='chg_profile_view'),
    path('edit_profile/', edit_account_view, name='edit_profile'),
    path('cart/', cart, name='cart'),
    path('to_cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('product_color/<str:model_product>/<str:color>', product_by_color, name='product_color'),
    path('clear_cart/', clear, name='clear_cart')
]