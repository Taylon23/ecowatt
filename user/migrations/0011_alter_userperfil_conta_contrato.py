# Generated by Django 5.1.4 on 2025-02-17 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_userperfil_conta_contrato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userperfil',
            name='conta_contrato',
            field=models.IntegerField(),
        ),
    ]
