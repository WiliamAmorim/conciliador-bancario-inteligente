import logging
from database.conexao import obter_conexao

logger = logging.getLogger(__name__)


def inserir_transacoes(df, origem, execucao_id):

    if df is None or df.empty:
        logger.warning(f"Nenhum dado para importar | Origem: {origem}")
        return

    conn = None
    cursor = None
    total_inseridos = 0
    total_erros = 0

    try:
        logger.info(
            f"Iniciando importação | Execução: {execucao_id} | Origem: {origem} | Registros: {len(df)}"
        )

        conn = obter_conexao()
        cursor = conn.cursor()

        sql = """
            INSERT INTO transacoes 
            (execucao_id, data_movimento, descricao, valor, tipo, categoria, origem)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        for _, linha in df.iterrows():

            try:
                valor = float(linha["valor"])
                tipo = "credito" if valor > 0 else "debito"

                valores = (
                    execucao_id,
                    linha["data"].date(),
                    linha["descricao"],
                    valor,
                    tipo,
                    linha.get("categoria", None),
                    origem
                )

                cursor.execute(sql, valores)
                total_inseridos += 1

            except Exception:
                total_erros += 1
                logger.exception(
                    f"Erro ao inserir registro | Execução: {execucao_id} | Descrição: {linha.get('descricao')}"
                )
                continue

        conn.commit()

        logger.info(
            f"Importação finalizada | Execução: {execucao_id} | Inseridos: {total_inseridos} | Erros: {total_erros}"
        )

    except Exception:
        if conn:
            conn.rollback()
            logger.warning("Rollback realizado na importação.")

        logger.exception("Erro crítico durante importação.")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            logger.info("Conexão encerrada após importação.")