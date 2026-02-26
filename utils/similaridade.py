from difflib import SequenceMatcher


def calcular_similaridade(texto1: str, texto2: str) -> float:
    """
    Retorna percentual de similaridade entre duas strings.
    """
    try:
        texto1 = (texto1 or "").lower()
        texto2 = (texto2 or "").lower()
        return SequenceMatcher(None, texto1, texto2).ratio() * 100
    except Exception: 
        logger.exception("Erro ao calcular similaridade.")
        raise