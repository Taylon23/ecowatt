# Generated by Django 5.1.4 on 2025-02-14 21:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_usertarefa_tarefa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertarefa',
            name='tarefa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.tarefa'),
        ),
    ]
