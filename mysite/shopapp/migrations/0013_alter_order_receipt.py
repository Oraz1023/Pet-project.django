# Generated by Django 5.0.3 on 2024-03-28 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0012_alter_product_options_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='receipt',
            field=models.FileField(blank=True, null=True, upload_to='orders/receipts'),
        ),
    ]