from difflib import SequenceMatcher
import logging
from utils.similaridade import calcular_similaridade

from config import (
    TOLERANCIA_CENTAVOS,
    TOLERANCIA_DIAS,
    SIMILARIDADE_MINIMA,
    SIMILARIDADE_AUTO
)

from database.transacoes import buscar_candidatos, marcar_conciliado
from database.conciliacoes import inserir_conciliacao

logger = logging.getLogger(__name__)


def executar_conciliacao(execucao_id):
    logger.info(f"Iniciando conciliação | Execução ID: {execucao_id}")

    try:
        # ✅ agora passa execucao_id
        candidatos = buscar_candidatos(
            execucao_id,
            TOLERANCIA_CENTAVOS,
            TOLERANCIA_DIAS
        )

        logger.info(f"{len(candidatos)} candidatos encontrados.")

    except Exception:
        logger.exception("Erro ao buscar candidatos para conciliação.")
        raise

    total_auto = 0
    total_sugestao = 0
    total_erros = 0

    for c in candidatos:

        try:
            id_extrato = c["id_extrato"]
            id_controle = c["id_controle"]
            desc_extrato = c["desc_extrato"]
            desc_controle = c["desc_controle"]
            diferenca_valor = c["diferenca_valor"]
            diferenca_dias = c["diferenca_dias"]

            similaridade = calcular_similaridade(
                desc_extrato,
                desc_controle
            )

            # 🔹 AUTO
            if similaridade >= SIMILARIDADE_AUTO:

                inserir_conciliacao(
                    execucao_id,
                    id_extrato,
                    id_controle,
                    diferenca_valor,
                    diferenca_dias,
                    similaridade,
                    "AUTO"
                )

                marcar_conciliado(id_extrato, id_controle)

                total_auto += 1

                logger.info(
                    f"[AUTO] Extrato {id_extrato} ↔ Controle {id_controle} | Similaridade: {similaridade:.2f}%"
                )

            # 🔹 SUGESTÃO
            elif similaridade >= SIMILARIDADE_MINIMA:

                inserir_conciliacao(
                    execucao_id,
                    id_extrato,
                    id_controle,
                    diferenca_valor,
                    diferenca_dias,
                    similaridade,
                    "SUGESTAO"
                )

                total_sugestao += 1

                logger.info(
                    f"[SUGESTAO] Extrato {id_extrato} ↔ Controle {id_controle} | Similaridade: {similaridade:.2f}%"
                )

        except Exception:
            total_erros += 1
            logger.exception(
                f"Erro ao processar candidato | Extrato: {c.get('id_extrato')} | Controle: {c.get('id_controle')}"
            )
            continue

    logger.info(
        f"Conciliação finalizada | AUTO: {total_auto} | SUGESTÕES: {total_sugestao} | ERROS: {total_erros}"
    )

    print("\n=== Conciliação Finalizada ===")
    print(f"Automáticos: {total_auto}")
    print(f"Sugestões: {total_sugestao}")
    print(f"Erros: {total_erros}")