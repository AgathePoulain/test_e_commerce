# Generated by Django 4.2.3 on 2023-07-31 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_item_formatted_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='formatted_price',
        ),
    ]
