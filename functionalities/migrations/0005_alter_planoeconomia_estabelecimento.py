# Generated by Django 5.1.3 on 2024-11-25 20:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functionalities', '0004_alter_planoeconomia_estabelecimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planoeconomia',
            name='estabelecimento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planos_economia', to='functionalities.estabelecimento', unique=True),
        ),
    ]
