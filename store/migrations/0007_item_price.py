# Generated by Django 4.2.3 on 2023-07-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_order_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
