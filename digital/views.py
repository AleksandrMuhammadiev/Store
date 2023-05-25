from random import randint

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Product, Category, FavoriteProducts, Profile, Gallery, SaveOrder, SaveOrderProducts
from .forms import LoginForm, RegistrationForm, CreateProfileForm, EditProfileForm, EditAccountForm, CustomerForm, \
    ShippingForm
from .filters import ProductFilter
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from .utils import *
from shop import settings
import stripe


# Create your views here.
class ProductList(ListView):
    model = Product
    context_object_name = 'categories'  # для вывода категорий

    extra_context = {
        'title': 'Digital Market'
    }
    template_name = 'digital/index.html'

    # Функ чтобы переназначить вывод что бы получать подкатегории определённой категории
    def get_queryset(self):
        categories = Category.objects.filter(parent=None)

        return categories


class CategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'digital/category_page.html'
    paginate_by = 3

    # метод для вывода товаров подкатегорий
    def get_queryset(self):
        brand_field = self.request.GET.get('brand')
        color_field = self.request.GET.get('color')
        price_field = self.request.GET.get('price')
        discount_field = self.request.GET.get('discount')

        category = Category.objects.get(slug=self.kwargs['slug'])  # получили главную категорию Часы
        products = Product.objects.filter(category=category)  # Все продукты всех субкатегорий
        if brand_field:
            products = products.filter(brand__title=brand_field)

        if color_field:
            products = products.filter(color_name=color_field)

        if price_field:
            products = products.filter(price=price_field)

        if discount_field:
            products = products.filter(discount=discount_field)

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)  # Все продукты всех субкатегорий
        myFilter = ProductFilter()
        brands = list(set([i.brand for i in products]))
        colors = list(set([i.color_name for i in products]))
        prices = list(set([int(i.price) for i in products]))
        discounts = list(set([i.discount for i in products]))

        context['brands'] = brands
        context['colors'] = colors
        context['discounts'] = discounts
        context['prices'] = sorted(prices)

        context['myFilter'] = myFilter
        context['category'] = category
        context['title'] = f'Категория: {category.title}'
        return context


def save_favorite_product(request, product_slug):
    user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(slug=product_slug)
    favorite_products = FavoriteProducts.objects.filter(user=user)
    if user:
        if product in [i.product for i in
                       favorite_products]:  # собираем все продукты в список,  делам генератором что выводить только продукт без пользователя
            fav_product = FavoriteProducts.objects.get(user=user, product=product)
            fav_product.delete()
        else:
            FavoriteProducts.objects.create(user=user, product=product)
    next_page = request.META.get('HTTP_REFERER', 'index')
    # HTTP_REFERER - это с какой страницы пришёл сигнал и перейдём либо на ту страницу что были или на главную
    return redirect(next_page)


#  ---------------------------------------------------------------------------------
# Функция для вывода избранного на страницу избранного
# LoginRequiredMixin # Данный класс служит что бы перекидывать пользователя на страницу Логина
class FavouriteProductsView(LoginRequiredMixin, ListView):
    model = FavoriteProducts
    context_object_name = 'products'
    template_name = 'digital/favourite_products.html'
    login_url = 'login'

    def get_queryset(self):
        user = self.request.user
        favs = FavoriteProducts.objects.filter(user=user)
        products = [i.product for i in favs]
        return products


class ProductDetail(DetailView):  # product_detail.html класс автоматом ищет
    model = Product
    context_object_name = 'product'

    # метод для шапки страницы Название
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])  # берём тот самый продукт который вытаскиваем
        context['title'] = f'Товар {product.title}'
        color = self.request.GET.get('color')
        print(color)
        if color:
            context['image'] = product.images.get(color=f'#{color}').image.url
        products = Product.objects.filter(category=product.category)  # берём все продукты
        data = []
        for i in range(len(products)):
            random_index = randint(0, len(products) - 1)  # для вывода рондома продуктов рекомендаций
            p = products[random_index]
            if p not in data and product != p:
                data.append(p)
        context['products'] = data

        return context


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user:
                    login(request, user)
                    return redirect('index')
                else:
                    return redirect('login')
            else:
                return redirect('login')
        else:
            form = LoginForm()
        context = {
            'form': form,
            'title': 'Вход в аккаунт'
        }
        return render(request, 'digital/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                # login(request, user)
                form2 = CreateProfileForm(request.POST, request.FILES)
                if form2.is_valid():
                    profile = form2.save(commit=False)
                    profile.user = user
                    profile.save()

                    messages.success(request, 'Вы успешно зарешистрированы. Войдите в аккаунт')
                    return redirect('index')
            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())
                    print(form.errors[field].as_text())
                return redirect('register')
        else:
            form = RegistrationForm()
            form2 = CreateProfileForm()
        context = {
            'form': form,
            'form2': form2,
            'title': 'Регистрация пользователя'
        }
        return render(request, 'digital/register.html', context)


def profile_view(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        orders = SaveOrder.objects.filter(customer_id=pk)
        context = {
            'profile': profile,
            'orders': orders
        }
        return render(request, 'digital/profile.html', context)
    else:
        return redirect('login')


# Функция для страницы изменения Аккаунта и профиля
def chg_profile_view(request):
    if request.user.is_authenticated:
        edit_account_form = EditAccountForm(instance=request.user if request.user.is_authenticated else None)
        edit_profile_form = EditProfileForm(instance=request.user.profile if request.user.is_authenticated else None)
        context = {
            'edit_account_form': edit_account_form,
            'edit_profile_form': edit_profile_form
        }
        return render(request, 'digital/chg_profile.html', context)
    else:
        return redirect('login')


# Функция для изменения Аккаунта и Профиля
@login_required
def edit_account_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EditAccountForm(request.POST, instance=request.user)
            form2 = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid() and form2.is_valid():
                data = form.cleaned_data
                form2.save()
                user = User.objects.get(id=request.user.id)
                if user.check_password(data['old_password']):
                    if data['old_password'] and data['new_password'] == data['confirm_password']:
                        user.set_password(data['new_password'])
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.warning(request, 'Пароль успшно изменён')
                        return redirect('profile', user.pk)
                    else:
                        for field in form.errors:
                            messages.error(request, form.errors[field].as_text())
                else:
                    for field in form.errors:
                        messages.error(request, form.errors[field].as_text())

                form.save()
            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())

            user = request.user
            return redirect('profile', user.pk)
    else:
        return redirect('login')


def cart(request):
    # как будит готов utils.py дописать логику
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)
        print(cart_info['products'])

        context = {
            'cart_total_quantity': cart_info['cart_total_quantity'],
            'order': cart_info['order'],
            'products': cart_info['products']
        }
        print(context)

        return render(request, 'digital/my_cart.html', context)
    else:
        return redirect('login')


# Функция возвращающая продукт по цвету
def product_by_color(request, model_product, color):
    product = Product.objects.get(model_product_id=model_product, color=color)
    products = Product.objects.filter(category=product.category)  # берём все продукты
    data = []
    for i in range(len(products)):
        random_index = randint(0, len(products) - 1)  # для вывода рондома продуктов рекомендаций
        p = products[random_index]
        if p not in data and product != p:
            data.append(p)

    context = {
        'product': product,
        'products': data
    }
    return render(request, 'digital/product_detail.html', context)


def to_cart(request, product_id, action):
    # как будит готов utils.py дописать логику
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, product_id, action)
        next_page = request.META.get('HTTP_REFERER', 'index')
        return redirect(next_page)
    else:
        messages.error(request, 'Авторизуйтесь или зарегистрируйтесь, что бы совершать покупки')
        return redirect('login_registration')


# Функция для очищения корзины
def clear(request):
    user_cart = CartForAuthenticatedUser(request)  # Рождаеться класс
    order = user_cart.get_cart_info()['order']  # получаю заказ
    order_products = order.orderproduct_set.all()  # получаю продукты заказа
    for order_product in order_products:  # прохожусь циклом по всем продуктам корзины
        quantity = order_product.quantity  # получаю кол-во
        product = order_product.product  # получаю продукты
        order_product.delete()  # удвляю  продукты заказа
        product.quantity += quantity  # продукты их количество влозврящаю в кол-во на склад
        product.save()  # сохраняю.
    messages.warning(request, 'Корзина очищена')
    return redirect('cart')


def checkout(request):
    # как будит готов utils.py дописать логику
    cart_info = get_cart_data(request)

    context = {
        # как будит готов utils.py дописать логику
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'order': cart_info['order'],
        'items': cart_info['products'],

        'customer_form': CustomerForm(),
        'shipping_form': ShippingForm(),
        'title': 'Оформление заказа'
    }
    return render(request, 'digital/checkout.html', context)


#  ---------------------------------------------------------------------------------
# Функция для проведения оплаты по stripe
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForAuthenticatedUser(request)  # Рождается класс Корзины
        cart_info = user_cart.get_cart_info()  # Получаем метод класса что бы получить данные о корзине
        order = cart_info['order']
        order_save = SaveOrder.objects.create(customer=order.customer, total_price=order.get_cart_total_price)
        order_save.save()
        order_products = order.orderproduct_set.all()
        for product in order_products:
            save_order_product = SaveOrderProducts.objects.create(order_id=order_save.pk,
                                                                  product=str(product),
                                                                  quantity=product.quantity,
                                                                  product_price=product.product.price,
                                                                  final_price=product.get_total_price,
                                                                  photo=product.product.get_first_photo(),
                                                                  color_name=product.product.color_name)
            print('Заказ готов')
            save_order_product.save()

        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.first_name = customer_form.cleaned_data['first_name']
            customer.last_name = customer_form.cleaned_data['last_name']
            customer.email = customer_form.cleaned_data['email']
            customer.save()
            user = User.objects.get(username=request.user.username)
            user.first_name = customer_form.cleaned_data['first_name']
            user.last_name = customer_form.cleaned_data['last_name']
            user.email = customer_form.cleaned_data['email']
            user.save()

        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()['order']
            address.save()
        else:
            for field in shipping_form.errors:
                messages.error(request, shipping_form.errors[field].as_text())
                print(shipping_form.errors[field].as_text())

        total_price = cart_info['cart_total_price']
        total_quantity = cart_info['cart_total_quantity']
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'товары с TOTEMBO'
                    },
                    'unit_amount': int(total_price)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('success'))
        )
        return redirect(session.url, 303)


def success_payment(request):
    user_cart = CartForAuthenticatedUser(request)
    user_cart.clear()
    messages.success(request, 'Оплата прошла успешно')
    return render(request, 'digital/success.html')



# def get_history_orders(request, pk):
#     orders = SaveOrder.objects.filter(customer_id=pk)
#     context = {
#
#     }
















