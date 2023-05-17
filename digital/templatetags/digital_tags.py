from django import template
from digital.models import Category, FavoriteProducts, Product, Gallery

register = template.Library()


# Функция для получений категорий
@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_products(category):
    return Product.objects.filter(category=category)[::-1]


@register.simple_tag()
def get_favorite_products(user):
    fav = FavoriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]  # делам генератором что выводить только продукт без пользователя
    return products


@register.simple_tag()
def get_normal_price(price):
    return f"{price:_} сум".replace("_", " ")


@register.simple_tag()
def return_color_product(model):
    p = Product.objects.filter(model_product=model)
    list_color = [i.color for i in p]
    return list_color




@register.simple_tag()
def product_by_color(request, model_product):
    product = Product.objects.filter(model_product=model_product)
    print(product)