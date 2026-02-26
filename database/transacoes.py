from database.conexao import obter_conexao
import logging

logger = logging.getLogger(__name__)


def buscar_candidatos(execucao_id, tolerancia_centavos, tolerancia_dias):

    conn = None
    cursor = None

    try:
        logger.info(
            f"Buscando candidatos | Execução: {execucao_id} | "
            f"Tolerância Valor: {tolerancia_centavos} | "
            f"Tolerância Dias: {tolerancia_dias}"
        )

        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT 
                e.id AS id_extrato,
                c.id AS id_controle,
                e.descricao AS desc_extrato,
                c.descricao AS desc_controle,
                e.valor AS valor_extrato,
                c.valor AS valor_controle,
                ABS(DATEDIFF(e.data_movimento, c.data_movimento)) AS diferenca_dias,
                ABS(e.valor - c.valor) AS diferenca_valor
            FROM transacoes e
            JOIN transacoes c
                ON e.tipo = c.tipo
                AND e.execucao_id = c.execucao_id
            WHERE e.execucao_id = %s
            AND e.origem = 'extrato'
            AND c.origem = 'controle'
            AND e.conciliado = 0
            AND c.conciliado = 0
            AND ABS(e.valor - c.valor) <= %s
            AND ABS(DATEDIFF(e.data_movimento, c.data_movimento)) <= %s
        """

        cursor.execute(sql, (execucao_id, tolerancia_centavos, tolerancia_dias))
        resultados = cursor.fetchall()

        logger.info(f"{len(resultados)} candidatos encontrados.")

        return resultados

    except Exception:
        logger.exception("Erro ao buscar candidatos.")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            logger.info("Conexão encerrada após buscar candidatos.")


def marcar_conciliado(id_extrato, id_controle):

    conn = None
    cursor = None

    try:
        logger.info(
            f"Marcando conciliado | Extrato: {id_extrato} | Controle: {id_controle}"
        )

        conn = obter_conexao()
        cursor = conn.cursor()

        sql = """
            UPDATE transacoes
            SET conciliado = 1
            WHERE id IN (%s, %s)
        """

        cursor.execute(sql, (id_extrato, id_controle))

        if cursor.rowcount != 2:
            logger.warning(
                f"Quantidade inesperada de registros atualizados: {cursor.rowcount}"
            )

        conn.commit()

        logger.info("Transações marcadas como conciliadas com sucesso.")

    except Exception:
        if conn:
            conn.rollback()
            logger.warning("Rollback realizado em marcar_conciliado().")

        logger.exception(
            f"Erro ao marcar conciliado | Extrato: {id_extrato} | Controle: {id_controle}"
        )
        raise

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            logger.info("Conexão encerrada após marcar conciliado.")