from database.conexao import obter_conexao
import logging

logger = logging.getLogger(__name__)


def inserir_conciliacao(execucao_id,
                        id_extrato,
                        id_controle,
                        diferenca_valor,
                        diferenca_dias,
                        similaridade,
                        status):

    conn = None
    cursor = None

    try:
        logger.info(
            f"Inserindo conciliação | Execução: {execucao_id} | "
            f"Extrato: {id_extrato} | Controle: {id_controle} | Status: {status}"
        )

        conn = obter_conexao()
        cursor = conn.cursor()

        sql = """
            INSERT INTO conciliacoes (
                execucao_id,
                lancamento_banco_id,
                lancamento_controle_id,
                diferenca_valor,
                diferenca_dias,
                similaridade,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            execucao_id,
            id_extrato,
            id_controle,
            diferenca_valor,
            diferenca_dias,
            similaridade,
            status
        ))

        conn.commit()

        logger.info("Conciliação inserida com sucesso.")

    except Exception:
        if conn:
            conn.rollback()
            logger.warning("Rollback realizado em inserir_conciliacao().")

        logger.exception(
            f"Erro ao inserir conciliação | Execução: {execucao_id} | "
            f"Extrato: {id_extrato} | Controle: {id_controle}"
        )
        raise

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            logger.info("Conexão encerrada após inserir conciliação.")

# Utilizado para gerar o relatório PDF
def buscar_conciliacoes_por_execucao(execucao_id):
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)

        sql = """
        SELECT 
            c.id,
            c.execucao_id,
            c.lancamento_banco_id,
            c.lancamento_controle_id,
            c.similaridade,
            c.status,
            tb.descricao AS descricao_extrato,
            tb.valor AS valor_extrato,
            tc.descricao AS descricao_controle,
            tc.valor AS valor_controle
        FROM conciliacoes c
        INNER JOIN transacoes tb
            ON c.lancamento_banco_id = tb.id
        INNER JOIN transacoes tc
            ON c.lancamento_controle_id = tc.id
        WHERE c.execucao_id = %s
        """

        cursor.execute(sql, (execucao_id,))
        resultado = cursor.fetchall()

        cursor.close()
        conexao.close()

        return resultado

    except Exception:
        logger.exception(
            f"Erro em buscar_conciliacoes_por_execucao() | execucao: {execucao_id}"
        )
        raise