# Generated by Django 4.2.3 on 2023-07-31 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_remove_item_formatted_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='items',
            new_name='orders',
        ),
    ]