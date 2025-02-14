from django.db import models
from django.contrib.auth.models import User
from .choices import PATENTES, DESCRICOES_PATENTES


class PerfilGamer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil')
    nivel = models.PositiveIntegerField(default=1)  # Nível atual
    experiencia = models.PositiveIntegerField(default=0)  # XP acumulada
    patente = models.CharField(
        max_length=50, choices=PATENTES, default='INICIANTE')  # Patente atual

    def __str__(self):
        return f"{self.user.username} - {self.get_patente_display()}"

    def calcular_nivel(self):
        """Calcula e atualiza o nível do jogador com base na experiência."""
        nivel_anterior = self.nivel  # Armazena o nível anterior para comparação
        self.nivel = self.experiencia // 50 + 1  # Calcula o novo nível

        if self.nivel != nivel_anterior:
            self.save()  # Salva as alterações no banco de dados
            return True  # Retorna True se o nível foi alterado
        return False  # Retorna False se o nível não foi alterado

    def atualizar_patente(self):
        """
        Atualiza a patente do usuário com base no nível.
        """
        novo_patente = None
        if self.nivel >= 150:
            novo_patente = 'LENDA'
        elif self.nivel >= 100:
            novo_patente = 'DOUTOR'
        elif self.nivel >= 70:
            novo_patente = 'MESTRE'
        elif self.nivel >= 50:
            novo_patente = 'ESPECIALISTA'
        elif self.nivel >= 35:
            novo_patente = 'ENGENHEIRO'
        elif self.nivel >= 20:
            novo_patente = 'TECNICO'
        elif self.nivel >= 10:
            novo_patente = 'APRENDIZ'
        else:
            novo_patente = 'INICIANTE'

        # Verifica se a patente mudou, se mudou, atribui
        if novo_patente != self.patente:
            self.patente = novo_patente
            
    def progresso_para_proximo_nivel(self):
        """
        Calcula o progresso em porcentagem para o próximo nível.
        """
        xp_necessario = 50  # XP necessário para subir de nível
        xp_atual = self.experiencia % xp_necessario  # XP acumulada no nível atual
        return (xp_atual / xp_necessario) * 100  # Retorna a porcentagem


    def save(self, *args, **kwargs):
        self.atualizar_patente()  # Garante que a patente esteja correta antes de salvar
        self.calcular_nivel()
        self.progresso_para_proximo_nivel()
        super().save(*args, **kwargs)


class Equipamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Tarefa(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    equipamentos = models.ManyToManyField(Equipamento, related_name='tarefas')
    passos_necessarios = models.PositiveIntegerField(default=1)
    pontos = models.PositiveIntegerField(
        default=0)  # Pontos que o desafio vale
    passo1 = models.TextField(blank=True, null=True)  # Passo 1
    passo2 = models.TextField(blank=True, null=True)  # Passo 2
    passo3 = models.TextField(blank=True, null=True)  # Passo 3
    passo4 = models.TextField(blank=True, null=True)  # Passo 4

    def __str__(self):
        return self.titulo


class UserEquipamento(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.equipamento.nome}"


class UserTarefa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tarefa = models.OneToOneField(Tarefa, on_delete=models.CASCADE,unique=True)
    passos_concluidos = models.PositiveIntegerField(default=0)
    completo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.tarefa.titulo}"

    def concluir_passo(self):
        """
        Marca um passo como concluído e verifica se a tarefa foi completada.
        """
        self.passos_concluidos += 1
        if self.passos_concluidos >= self.tarefa.passos_necessarios:
            self.completo = True
            # Adiciona pontos ao perfil do usuário
            perfil, created = PerfilGamer.objects.get_or_create(user=self.user)
            perfil.experiencia += self.tarefa.pontos
            perfil.save()
        self.save()


class TextoDicas(models.Model):
    texto = models.CharField(max_length=300,blank=False)