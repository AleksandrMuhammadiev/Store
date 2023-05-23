# Generated by Django 4.2.1 on 2023-05-19 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digital', '0036_brand_category_modelproduct_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='comment',
            field=models.TextField(default=1, verbose_name='Коментарий к заказу'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='digital.customer', verbose_name='Покупатель'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='digital.order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='phone',
            field=models.CharField(max_length=255, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='state',
            field=models.CharField(max_length=255, verbose_name='Регион'),
        ),
    ]
