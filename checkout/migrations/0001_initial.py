# Generated by Django 3.2.6 on 2021-09-13 12:47

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CheckoutOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=32)),
                ('deliver_to_name', models.CharField(max_length=60)),
                ('buyer_name', models.CharField(max_length=60)),
                ('email_address', models.EmailField(max_length=254)),
                ('street_address', models.CharField(max_length=254)),
                ('town_or_city', models.CharField(max_length=254)),
                ('county', models.CharField(blank=True, max_length=254, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('zip_postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('order_total', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
            ],
        ),
    ]
