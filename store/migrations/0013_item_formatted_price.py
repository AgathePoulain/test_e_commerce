# Generated by Django 4.2.3 on 2023-07-31 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_order_ordered_order_ordered_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='formatted_price',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]