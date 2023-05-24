from .models import Product, OrderProduct, Order, Customer


# Класс который будит отвечать за всю корзину и создавать и выводить данные
class CartForAuthenticatedUser:
    def __init__(self, request, product_id=None, action=None):
        self.user = request.user

        if product_id and action:
            self.add_or_delete(product_id, action)

    # Метод который будит возвращать инфо о корзине
    def get_cart_info(self):
        # пытается получить по параметрам пользователя если нет то создаёт
        customer, created = Customer.objects.get_or_create(
            user=self.user,

        )
        order, created = Order.objects.get_or_create(customer=customer)
        order_products = order.orderproduct_set.all()

        cart_total_quantity = order.get_cart_total_quantity
        cart_total_price = order.get_cart_total_price

        return {
            'cart_total_quantity': cart_total_quantity,
            'cart_total_price': cart_total_price,
            'order': order,
            'products': order_products
        }



    # Метод который будит добавлять и удалять товар
    def add_or_delete(self, product_id, action):
        oder = self.get_cart_info()['order']
        product = Product.objects.get(pk=product_id)
        order_product, created = OrderProduct.objects.get_or_create(order=oder, product=product)  # получить или создать

        if action == 'add' and product.quantity > 0:  # Если на складе больше нуля
            order_product.quantity += 1  # +1 в корзине
            product.quantity -= 1  # -1 на складе
        else:  # delete
            order_product.quantity -= 1
            product.quantity += 1
        product.save()
        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()


    # Метод который будит очищать корзину
    def clear(self):
        order = self.get_cart_info()['order']
        order_products = order.orderproduct_set.all()
        for product in order_products:
            product.delete()
        order.save()


# Функция для анонимного пользователя
def get_cart_data(request):
    cart = CartForAuthenticatedUser(request)
    cart_info = cart.get_cart_info()
    return {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'cart_total_price': cart_info['cart_total_price'],
        'order': cart_info['order'],
        'products': cart_info['products']
    }







