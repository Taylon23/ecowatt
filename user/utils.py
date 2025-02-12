""" def gerar_cupom(user):
    perfil = user.perfil_energia
    if perfil.cupom:  # Verifica se já existe um cupom
        return perfil.cupom  # Retorna o cupom existente

    # Gera um novo cupom apenas se não houver um já existente
    import uuid
    cupom = str(uuid.uuid4()).split('-')[0].upper()
    perfil.cupom = cupom
    perfil.save()
    return cupom """