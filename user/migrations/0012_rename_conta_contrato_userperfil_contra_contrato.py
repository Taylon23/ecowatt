# Generated by Django 5.1.4 on 2025-02-17 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_userperfil_conta_contrato'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userperfil',
            old_name='conta_contrato',
            new_name='contra_contrato',
        ),
    ]
