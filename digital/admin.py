from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin

from .models import *
from django.utils.safestring import mark_safe
from .forms import CategoryForm


# Register your models here.


class GalleryInline(admin.TabularInline):  # данный класс служит как доп параметр для добавления нескольких фото товару
    fk_name = 'product'
    model = Gallery
    extra = 1


class ParameterInline(admin.TabularInline):  # данный класс служит как доп параметр для добавления нескольких фото товару
    fk_name = 'product'
    model = ProductDescription
    extra = 1


class CreditInline(admin.TabularInline):  # данный класс служит как доп параметр для добавления нескольких фото товару
    fk_name = 'product'
    model = Credit
    extra = 1

class SaveProductInline(admin.TabularInline):  # данный класс служит как доп параметр для добавления нескольких фото товару
    fk_name = 'order'
    model = SaveOrderProducts
    extra = 1



# Регистрация модельки категории в Админке
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
    'title', 'parent', 'get_products_count', 'get_photo')  # добавить get_products_count в кортеж как будит готова функ
    prepopulated_fields = {'slug': ('title',)}  # параметр для автоматического заполнения поля slug
    form = CategoryForm

    def get_photo(self, obj):  # функция для получения миниатюры картинки в Админке
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'

    # Данную функцию сделать после того как будут готовы классы  CategoryAdmin GalleryInline ProductAdmin
    # Функция позволит видеть в Админке кол-во товара категории
    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_products_count.short_description = 'Количество товаров'  # что бы в Админке было на Русском


# Регистрация модельки продукта в Админке
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'created_at',
                    'get_photo')  # get_photo добавить после того как будит готова функ
    list_editable = ('price', 'quantity')  # то что можно быстро менять в Админке
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price', 'category', 'model_product')
    inlines = [GalleryInline, ParameterInline, CreditInline]

    def get_photo(self, obj):  # функция для получения миниатюры картинки в Админке
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity', 'get_total_price']

@admin.register(SaveOrder)
class SaveOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer','total_price', 'created_at']
    inlines = [SaveProductInline]


admin.site.register(Gallery)
admin.site.register(FavoriteProducts)
admin.site.register(Brand)
admin.site.register(Profile)

admin.site.register(Customer)
admin.site.register(Order)
# admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
admin.site.register(City)
admin.site.register(ModelProduct)

#
# admin.site.register(SaveOrder)
admin.site.register(SaveOrderProducts)


