from .models import Ajuste
from .choice import HORAS_RECOMENDADAS


class DicasEconomia:

    def __init__(self, estabelecimento):
        self.estabelecimento = estabelecimento
        self.plano = estabelecimento.planos_economia
        self.equipamentos = estabelecimento.equipamentos.all()
        self.meta_gasto = estabelecimento.planos_economia.meta_gasto_mensal

    def calcular_dicas(self):
        dicas = []

        # Calcular dicas gerais baseadas nas metas e no consumo atual
        if self.plano:
            if self.plano.diferenca_custo > 0:
                dicas.append(
                    f"Ainda há {self.plano.diferenca_custo:.2f} R$ disponível para atingir sua meta de gasto.")
            else:
                dicas.append(
                    f"Você ultrapassou sua meta de gasto em {abs(self.plano.diferenca_custo):.2f} R$!")

            if self.plano.diferenca_kwh:
                if self.plano.diferenca_kwh > 0:
                    dicas.append(
                        f"Ainda há {self.plano.diferenca_kwh:.2f} kWh disponível para atingir sua meta de consumo.")
                else:
                    dicas.append(
                        f"Você ultrapassou sua meta de consumo em {abs(self.plano.diferenca_kwh):.2f} kWh!")

        # Dicas personalizadas para os tipos de equipamentos
        dicas_equipamentos = []

        for equipamento in self.equipamentos:
            if equipamento.tipo == 'geladeira':
                dicas_equipamentos.append(
                    "Geladeiras consomem muita energia, verifique a vedação da porta e evite abrir com frequência.")
            elif equipamento.tipo == 'tv':
                dicas_equipamentos.append(
                    "Reduza o brilho da TV para economizar energia, e considere desligar quando não estiver assistindo.")
            elif equipamento.tipo == 'ar_condicionado':
                dicas_equipamentos.append(
                    "Ar condicionado consome bastante energia. Ajuste a temperatura para 24°C e use ventiladores para auxiliar.")
            elif equipamento.tipo == 'maquina_lavar':
                dicas_equipamentos.append(
                    "Máquinas de lavar são mais eficientes com carga cheia. Evite lavagens frequentes de pequenas quantidades.")
            elif equipamento.tipo == 'microondas':
                dicas_equipamentos.append(
                    "O micro-ondas consome muita energia, utilize-o com sabedoria e prefira utilizar outros métodos de aquecer alimentos.")
            elif equipamento.tipo == 'computador':
                dicas_equipamentos.append(
                    "Desligue o computador ao não utilizá-lo por longos períodos, e ajuste as configurações de energia para reduzir o consumo.")
            elif equipamento.tipo == 'chuveiro_eletrico':
                dicas_equipamentos.append(
                    "Chuveiros elétricos consomem muito. Reduza o tempo de banho e prefira temperaturas mais amenas para economizar.")
            elif equipamento.tipo == 'ventilador':
                dicas_equipamentos.append(
                    "Ventiladores consomem menos energia que ar condicionados, mas ainda assim devem ser desligados quando não estiver em uso.")
            elif equipamento.tipo == 'forno_eletrico':
                dicas_equipamentos.append(
                    "Forno elétrico consome muita energia. Use-o com o máximo de alimentos possível para otimizar o consumo.")
            elif equipamento.tipo == 'luminaria_led':
                dicas_equipamentos.append(
                    "Luminárias LED são eficientes em termos de energia. Certifique-se de substituir lâmpadas antigas por modelos LED.")
            elif equipamento.tipo == 'ferro_passar':
                dicas_equipamentos.append(
                    "O ferro de passar consome bastante energia. Passe roupas em maior quantidade de uma vez e utilize a temperatura adequada.")

        # Agora, as dicas específicas dos equipamentos são adicionadas à lista principal
        dicas.extend(dicas_equipamentos)

        return dicas

    def calcular_consumo_total(self):
        # Calcula o consumo total mensal de todos os equipamentos
        return sum(equipamento.consumoMensalKwh for equipamento in self.equipamentos)

    def aplicar_ajustes(self):
        ajustes = []
        consumo_total_atual = self.calcular_consumo_total()
        custo_total_atual = sum(
            equipamento.custoMensal for equipamento in self.equipamentos)

        if custo_total_atual <= self.meta_gasto:
            # Se o consumo já está dentro da meta, só ajusta as horas para a média
            for equipamento in self.equipamentos:
                horas_recomendadas = HORAS_RECOMENDADAS.get(
                    equipamento.tipo, 1)
                equipamento.horas_por_dia = horas_recomendadas
                equipamento.save()
                ajustes.append(
                    f"As horas de uso do equipamento '{equipamento.nome_personalizado}' foram ajustadas para {horas_recomendadas} horas por dia.")
        else:
            # Caso o custo ultrapasse a meta de gasto, precisamos ajustar as horas de todos os equipamentos
            # Proporção do gasto que precisa ser reduzida
            fator_redução = self.meta_gasto / custo_total_atual
            novo_custo_total = 0

            for equipamento in self.equipamentos:
                horas_recomendadas = HORAS_RECOMENDADAS.get(
                    equipamento.tipo, 1)
                # Ajustar as horas para reduzir o custo
                horas_ajustadas = horas_recomendadas * fator_redução
                novo_custo_total += equipamento.potencia * horas_ajustadas * \
                    equipamento.tarifa_por_kwh / 1000  # Calcular o novo custo

                # Atualiza a quantidade de horas do equipamento
                equipamento.horas_por_dia = horas_ajustadas
                equipamento.save()
                ajustes.append(
                    f"As horas de uso do equipamento '{equipamento.nome_personalizado}' foram ajustadas para {horas_ajustadas:.2f} horas por dia para atender à meta de gasto.")

            # Se o custo total ajustado ainda estiver abaixo da meta, podemos tentar aumentar alguns equipamentos
            if novo_custo_total < self.meta_gasto:
                ajuste_extra = self.meta_gasto - novo_custo_total
                for equipamento in self.equipamentos:
                    # Distribuir o restante do custo extra de forma proporcional
                    horas_extra = ajuste_extra / \
                        len(self.equipamentos) / equipamento.potencia
                    equipamento.horas_por_dia += horas_extra
                    equipamento.save()
                    ajustes.append(
                        f"Ajuste extra nas horas do equipamento '{equipamento.nome_personalizado}' para {equipamento.horas_por_dia:.2f} horas por dia para otimizar o consumo.")

        # Registrar os ajustes realizados
        descricao_ajustes = "\n".join(ajustes)
        ajuste = Ajuste(
            estabelecimento=self.estabelecimento,
            descricao=descricao_ajustes
        )
        ajuste.save()

        return ajustes
