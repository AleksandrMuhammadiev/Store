from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, SaveOrder



# @receiver(post_save, sender=Order, dispatch_uid="govno")
# def update_stock(sender, instance: Order, **kwargs):
#     print('Что-то')
#     if instance.is_completed:
#         order = instance
#         order_products = instance.orderproduct_set.all()
#         for product in order_products:
#             save_order = SaveOrder.objects.create(order=order,
#                                                   product=product,
#                                                   quantity=product.quantity,
#                                                   product_price=product.product.price,
#                                                   final_price=product.get_total_price)
#             print('Заказ готов')
#             save_order.save()
#     else:
#         pass