TIPOS_EQUIPAMENTO = [
    ('geladeira', 'Geladeira'),
    ('tv', 'TV'),
    ('ar_condicionado', 'Ar Condicionado'),
    ('maquina_lavar', 'Máquina de Lavar'),
    ('microondas', 'Micro-ondas'),
    ('computador', 'Computador'),
    ('chuveiro_eletrico', 'Chuveiro Elétrico'),
    ('ventilador', 'Ventilador'),
    ('forno_eletrico', 'Forno Elétrico'),
    ('luminaria_led', 'Luminária LED'),
    ('ferro_passar', 'Ferro de Passar'),
]

HORAS_RECOMENDADAS = {
    'geladeira': 24,  # Sempre ligada
    'tv': 12,  # Média de 12 horas por dia
    'ar_condicionado': 8,  # Ligado durante a noite (8 horas)
    'maquina_lavar': 1,  # Uma vez por semana, mas vamos considerar 1 hora por dia
    'microondas': 0.5,  # Média de 30 minutos por dia
    'computador': 8,  # Ligado durante o dia, mais ou menos
    'chuveiro_eletrico': 0.5,  # 30 minutos por dia
    'ventilador': 7,  # Durante a noite (6 horas)
    'forno_eletrico': 1,  # 1 hora por dia
    'luminaria_led': 9,  # Média de 5 horas por dia
    'ferro_passar': .5,  # 1 hora por dia (considerando o uso de uma vez por semana, mas uma média de 1 hora por dia)
}
