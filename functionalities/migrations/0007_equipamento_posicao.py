# Generated by Django 5.1.3 on 2024-11-25 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functionalities', '0006_alter_planoeconomia_estabelecimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipamento',
            name='posicao',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
