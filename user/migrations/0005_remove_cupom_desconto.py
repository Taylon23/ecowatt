# Generated by Django 5.1.4 on 2025-02-11 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_userperfil_cupom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cupom',
            name='desconto',
        ),
    ]
