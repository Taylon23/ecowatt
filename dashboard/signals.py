from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PerfilGamer,UserDesafio


@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        PerfilGamer.objects.create(user=instance)
        

""" @receiver(post_save, sender=UserDesafio)
def atualizar_pontos_ao_concluir(sender, instance, created, **kwargs):
    if instance.completo:
        perfil, created = PerfilGamer.objects.get_or_create(user=instance.user)
        
        # Adiciona XP e atualiza nível/patente
        perfil.adicionar_xp(instance.desafio.pontos)
        
        # O método adicionar_xp já cuida do save, então não precisa repetir """