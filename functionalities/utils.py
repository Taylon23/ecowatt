from .models import Ajuste

class DicasEconomia:

    def __init__(self, estabelecimento):
        self.estabelecimento = estabelecimento
        self.plano = estabelecimento.planos_economia
        self.equipamentos = estabelecimento.equipamentos.all()
        self.meta_gasto = estabelecimento.planos_economia.meta_gasto_mensal

    def calcular_dicas(self):
        dicas = []

        # Dicas gerais baseadas nas metas e no consumo atual
        if self.plano:
            if self.plano.diferenca_custo > 0:
                dicas.append(
                    f"Você ainda pode gastar {self.plano.diferenca_custo:.2f} R$ para atingir sua meta de gasto mensal.")
            else:
                dicas.append(
                    f"Atenção! Você ultrapassou sua meta de gasto em {abs(self.plano.diferenca_custo):.2f} R$.")

            if self.plano.diferenca_kwh:
                if self.plano.diferenca_kwh > 0:
                    dicas.append(
                        f"Você ainda pode consumir {self.plano.diferenca_kwh:.2f} kWh para atingir sua meta de consumo.")
                else:
                    dicas.append(
                        f"Atenção! Você ultrapassou sua meta de consumo em {abs(self.plano.diferenca_kwh):.2f} kWh.")

        # Dicas personalizadas para os tipos de equipamentos
        for equipamento in self.equipamentos:
            dicas_equipamento = self._gerar_dicas_para_equipamento(equipamento)
            dicas.extend(dicas_equipamento)

        return dicas

    def _gerar_dicas_para_equipamento(self, equipamento):
        dicas = []
        horas_atual = equipamento.horas_por_dia
        potencia = equipamento.potencia  # Supondo que o modelo tenha um campo 'potencia' em watts

        # Consumo diário em kWh
        consumo_diario = (potencia * horas_atual) / 1000

        # Dicas específicas para cada equipamento
        if equipamento.tipo == 'geladeira':
            if horas_atual > 10:
                dicas.append(
                    f"Geladeira: Ajustamos o uso de {horas_atual} horas para 10 horas por dia. "
                    "Motivo: A geladeira fica ligada 24 horas, mas o compressor só funciona por cerca de 10 horas. "
                    "Dicas extras: Verifique a vedação da porta, evite abrir com frequência e mantenha a temperatura entre 3°C e 5°C."
                )
            else:
                dicas.append(
                    f"Geladeira: O uso está dentro do esperado (10 horas por dia para o compressor). "
                    "Dicas extras: Mantenha a temperatura ideal e evite colocar alimentos quentes."
                )

        elif equipamento.tipo == 'tv':
            if horas_atual > 4:
                dicas.append(
                    f"TV: Reduza o uso de {horas_atual} horas para 4 horas por dia. "
                    "Motivo: Assistir TV por muitas horas aumenta o consumo de energia. "
                    "Dicas extras: Reduza o brilho da tela e ative o modo de economia de energia."
                )
            else:
                dicas.append(
                    f"TV: O uso está dentro do recomendado (4 horas por dia). "
                    "Dicas extras: Desligue a TV quando não estiver assistindo."
                )

        elif equipamento.tipo == 'ar_condicionado':
            if horas_atual > 8:
                dicas.append(
                    f"Ar-condicionado: Reduza o uso de {horas_atual} horas para 8 horas por dia. "
                    "Motivo: O ar-condicionado consome muita energia quando usado por longos períodos. "
                    "Dicas extras: Ajuste a temperatura para 24°C e use ventiladores para auxiliar na circulação de ar."
                )
            else:
                dicas.append(
                    f"Ar-condicionado: O uso está dentro do recomendado (8 horas por dia). "
                    "Dicas extras: Mantenha os filtros limpos para melhorar a eficiência."
                )

        elif equipamento.tipo == 'maquina_lavar':
            if horas_atual > 0.5:
                dicas.append(
                    f"Máquina de lavar: Reduza o uso de {horas_atual} horas para 0.5 horas por dia. "
                    "Motivo: Usar a máquina com carga cheia e ciclos curtos economiza energia. "
                    "Dicas extras: Prefira água fria e use a máquina 2-3 vezes por semana."
                )
            else:
                dicas.append(
                    f"Máquina de lavar: O uso está dentro do recomendado (0.5 horas por dia). "
                    "Dicas extras: Use sempre com carga cheia."
                )

        elif equipamento.tipo == 'microondas':
            if horas_atual > 0.5:
                dicas.append(
                    f"Micro-ondas: Reduza o uso de {horas_atual} horas para 0.5 horas por dia. "
                    "Motivo: O micro-ondas consome muita energia quando usado por longos períodos. "
                    "Dicas extras: Use apenas o tempo necessário para aquecer os alimentos."
                )
            else:
                dicas.append(
                    f"Micro-ondas: O uso está dentro do recomendado (0.5 horas por dia). "
                    "Dicas extras: Evite abrir a porta durante o funcionamento."
                )

        # Adicione mais equipamentos conforme necessário...

        return dicas

    def calcular_consumo_total(self):
        # Calcula o consumo total mensal de todos os equipamentos
        consumo_total = 0
        for equipamento in self.equipamentos:
            horas_atual = equipamento.horas_por_dia
            potencia = equipamento.potencia
            consumo_diario = (potencia * horas_atual) / 1000
            consumo_mensal = consumo_diario * 30  # Considerando 30 dias no mês
            consumo_total += consumo_mensal
        return consumo_total

    def aplicar_ajustes(self):
        ajustes = []
        for equipamento in self.equipamentos:
            # Gerar dicas específicas para o equipamento
            dicas = self._gerar_dicas_para_equipamento(equipamento)
            
            # Registrar o ajuste para o equipamento atual
            descricao_ajustes = "\n".join(dicas)
            ajuste = Ajuste(
                estabelecimento=self.estabelecimento,
                equipamento=equipamento,  # Associar o ajuste ao equipamento
                descricao=descricao_ajustes
            )
            ajuste.save()

            # Adicionar as dicas à lista de ajustes para retorno
            ajustes.extend(dicas)

        return ajustes