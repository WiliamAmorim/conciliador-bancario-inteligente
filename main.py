from leitor import carregar_extrato, carregar_controle
from importador import inserir_transacoes
from services.motor_conciliacao import executar_conciliacao
from database.execucoes import criar_execucao, resumo_execucao
from config import (
    TOLERANCIA_CENTAVOS,
    TOLERANCIA_DIAS,
    SIMILARIDADE_MINIMA,
    PASTA_ENTRADA,
    PASTA_PROCESSADOS,
    PASTA_ERRO
)

import os
import shutil
import logging
from services.relatorio_pdf import gerar_relatorio_pdf
from utils.logger import configurar_logger

configurar_logger()
logger = logging.getLogger(__name__)


def processar_arquivos(execucao_id):

    try:
        arquivos = os.listdir(PASTA_ENTRADA)

        if not arquivos:
            logger.warning("Nenhum arquivo encontrado na pasta de entrada.")
            return False

    except Exception as e:
        logger.error(f"Erro ao acessar pasta de entrada: {e}")
        raise

    arquivos_processados = False

    for arquivo in arquivos:

        caminho = os.path.join(PASTA_ENTRADA, arquivo)

        try:
            logger.info(f"Processando arquivo: {arquivo}")

            if arquivo.endswith(".csv"):
                df = carregar_extrato(caminho)
                inserir_transacoes(df, "extrato", execucao_id)

            elif arquivo.endswith(".xlsx"):
                df = carregar_controle(caminho)
                inserir_transacoes(df, "controle", execucao_id)

            else:
                logger.warning(f"Formato não suportado: {arquivo}")
                continue

            shutil.move(caminho, os.path.join(PASTA_PROCESSADOS, arquivo))
            logger.info(f"Arquivo processado com sucesso: {arquivo}")
            arquivos_processados = True

        except Exception as e:
            logger.error(f"Erro ao processar arquivo {arquivo}: {e}")

            try:
                shutil.move(caminho, os.path.join(PASTA_ERRO, arquivo))
                logger.info(f"Arquivo movido para pasta de erro: {arquivo}")
            except Exception as erro_movimento:
                logger.critical(f"Erro ao mover arquivo para pasta de erro: {erro_movimento}")

    return arquivos_processados


def main():

    logger.info("Sistema iniciado")

    try:
        # ✅ 1) Criar execução primeiro
        execucao_id = criar_execucao(
            TOLERANCIA_CENTAVOS,
            TOLERANCIA_DIAS,
            SIMILARIDADE_MINIMA
        )

        logger.info(f"Execução criada com ID: {execucao_id}")

        # ✅ 2) Processar arquivos vinculando à execução
        houve_importacao = processar_arquivos(execucao_id)

        if not houve_importacao:
            logger.warning("Nenhum arquivo válido importado. Encerrando execução.")
            return

        # ✅ 3) Conciliar
        executar_conciliacao(execucao_id)

        # ✅ 4) Resumo
        resumo_execucao(execucao_id)

        # ✅ 5) Gerar PDF
        gerar_relatorio_pdf(execucao_id)

        logger.info("Sistema finalizado com sucesso.")

    except Exception as e:
        logger.critical(f"Erro crítico na execução principal: {e}", exc_info=True)
        print("Erro crítico. Verifique o log.")


if __name__ == "__main__":
    main()