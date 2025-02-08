# Generated by Django 5.1.4 on 2025-02-08 20:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_profile_pontos'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPerfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=220)),
                ('cpf', models.CharField(help_text='CPF do usuário', max_length=14)),
                ('data_nascimento', models.DateField(help_text='Data de nascimento do usuário')),
                ('cep', models.CharField(help_text='CEP do usuário', max_length=9)),
                ('endereco', models.CharField(blank=True, help_text='Endereço completo', max_length=220, null=True)),
                ('estado', models.CharField(blank=True, help_text='Estado da instalação (ex: PI)', max_length=2, null=True)),
                ('cidade', models.CharField(blank=True, help_text='Cidade do usuário', max_length=100, null=True)),
                ('token', models.CharField(blank=True, help_text='Token de autenticação', max_length=255, null=True)),
                ('consumo_atual', models.FloatField(default=0, help_text='Consumo atual em kWh')),
                ('consumo_anterior', models.FloatField(default=0, help_text='Consumo anterior em kWh')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_energia', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
