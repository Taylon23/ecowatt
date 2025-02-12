from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserPerfil, ConsumoMensal
from django.db.models.signals import post_delete, pre_save
import os
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Cria um perfil (UserPerfil) automaticamente quando um novo usuário é criado.
    """
    if created:
        # Cria o perfil associado ao usuário
        UserPerfil.objects.create(usuario=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Salva o perfil sempre que o usuário é salvo.
    """
    if hasattr(instance, 'perfil_energia'):  # Verifica se o perfil existe
        instance.perfil_energia.save()  # Salva o perfil associado ao usuário

# Sinal para excluir a imagem antiga ao atualizar o perfil


@receiver(pre_save, sender=UserPerfil)
def excluir_foto_antiga(sender, instance, **kwargs):
    if instance.pk:  # Verifica se o objeto já existe no banco de dados
        try:
            perfil_antigo = UserPerfil.objects.get(pk=instance.pk)
            if perfil_antigo.foto and perfil_antigo.foto != instance.foto:
                if os.path.isfile(perfil_antigo.foto.path):
                    os.remove(perfil_antigo.foto.path)
        except UserPerfil.DoesNotExist:
            pass

# Sinal para excluir a imagem ao excluir o perfil


@receiver(post_delete, sender=UserPerfil)
def excluir_foto_ao_deletar(sender, instance, **kwargs):
    if instance.foto:
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)
            
