# Generated by Django 5.1.4 on 2025-02-17 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_rename_conta_contrato_userperfil_contra_contrato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userperfil',
            name='contra_contrato',
            field=models.IntegerField(null=True),
        ),
    ]
