# Generated by Django 4.2.1 on 2023-05-19 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digital', '0037_shippingaddress_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта покупателя'),
        ),
    ]