from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from colorfield.fields import ColorField

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Категория')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Изображение категории')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               verbose_name='Категория',
                               related_name='subcategories')

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://vodanova.ru/wp-content/uploads/2022/04/Fotografija-skoro-pojavitsja.jpg'

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Категория: pk={self.pk}, title={self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование товара')
    model_product = models.ForeignKey('ModelProduct', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Модель')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    quantity = models.IntegerField(default=0, verbose_name='В наличии')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Категория',
                                 related_name='products')
    slug = models.SlugField(unique=True, null=True)
    color = ColorField(default='#FF0000', verbose_name='Цвет', blank=True, null=True)
    color_name = models.CharField(max_length=100, default='Белый', verbose_name='Цвет', blank=True, null=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Бренд')
    discount = models.IntegerField(verbose_name='Скидка', blank=True, null=True)
    memory = models.CharField(max_length=255 ,verbose_name='Пямать', blank=True)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return 'https://vodanova.ru/wp-content/uploads/2022/04/Fotografija-skoro-pojavitsja.jpg'
        else:
            return 'https://vodanova.ru/wp-content/uploads/2022/04/Fotografija-skoro-pojavitsja.jpg'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Изображения')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея товаров'





class FavoriteProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователи')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Избранный товар')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'




class Brand(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование Бренда')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name='Категория',
                                 related_name='brand')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

class ModelProduct(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование модели')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True, null=True,
                                 verbose_name='Категория',
                                 related_name='model_product')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'





class ProductDescription(models.Model):
    parameter = models.CharField(max_length=255, verbose_name='Название параметра')
    parameter_info = models.CharField(max_length=500, verbose_name='Описание параметра')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='parameters')

    class Meta:
        verbose_name = 'Описание товара'
        verbose_name_plural = 'Описание товаров'

class Credit(models.Model):
    from_price = models.IntegerField(default=0, verbose_name='От какой стоимости')
    month = models.IntegerField(default=0, verbose_name='Месяцы')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='credits')

    class Meta:
        verbose_name = 'Товар в рассрочку'
        verbose_name_plural = 'Товары в рассрочку'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user.username


    def get_photo(self):
        try:
            return self.photo.url
        except:
            return 'https://cs6.pikabu.ru/avatars/301/v301065.jpg'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'








class Customer(models.Model):
    user = models.OneToOneField(User, models.SET_NULL, blank=True, null=True)  # если удалиться юзер то обнулится
    first_name = models.CharField(max_length=255, default='', verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=255,default='', verbose_name='Фамилия пользователя')

    def __str__(self):
        return self.first_name


    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

# ----------------------------------------------------------------------------------------
# Моделька Заказа
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)  # завершён ли он
    shipping = models.BooleanField(default=True)  # доставка

    def __str__(self):
        return str(self.pk) + ' '  # для отображения в Админке

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property  # метод который подсчитывает общую стоимость заказа
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])  # считаем обш стоимость чека
        return total_price

    @property  # метод который подсчитывает общее кол-во товара
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity




# ----------------------------------------------------------------------------------------
# Моделька Заказанных продуктов (строчки товаров)
class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    addet_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'

    # Метод который может сам всё считать на каждый товар
    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


# ----------------------------------------------------------------------------------------
# Моделька Адрес доставки
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Города')  # City поставили в кавычках так как класс был создан позже
    state = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'



class City(models.Model):
    city_name = models.CharField(max_length=255, verbose_name='Название города')

    def __str__(self):
        return self.city_name


    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


































