# Generated by Django 3.2.6 on 2021-09-23 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0011_alter_checkoutorder_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkoutorder',
            old_name='user',
            new_name='profile',
        ),
    ]
