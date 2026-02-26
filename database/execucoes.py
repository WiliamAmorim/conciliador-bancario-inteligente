from database.conexao import obter_conexao
import logging

logger = logging.getLogger(__name__)


def criar_execucao(tolerancia_centavos,
                   tolerancia_dias,
                   similaridade_minima):

    conn = None
    cursor = None

    try:
        logger.info("Criando nova execução no banco.")

        conn = obter_conexao()
        cursor = conn.cursor()

        sql = """
            INSERT INTO execucoes (
                data_execucao,
                tolerancia_centavos,
                tolerancia_dias,
                similaridade_minima
            )
            VALUES (NOW(), %s, %s, %s)
        """

        cursor.execute(sql, (
            tolerancia_centavos,
            tolerancia_dias,
            similaridade_minima
        ))

        conn.commit()

        execucao_id = cursor.lastrowid

        logger.info(f"Execução criada com sucesso | ID: {execucao_id}")

        return execucao_id

    except Exception:
        if conn:
            conn.rollback()
            logger.warning("Rollback realizado ao criar execução.")

        logger.exception("Erro ao criar execução.")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            logger.info("Conexão encerrada após criar execução.")


def resumo_execucao(execucao_id):

    conn = None
    cursor = None

    try:
        logger.info(f"Gerando resumo da execução | ID: {execucao_id}")

        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT status, COUNT(*) as total
            FROM conciliacoes
            WHERE execucao_id = %s
            GROUP BY status
        """

        cursor.execute(sql, (execucao_id,))
        resultados = cursor.fetchall()

        total_auto = 0
        total_sugestao = 0

        for r in resultados:
            if r["status"] == "AUTO":
                total_auto = r["total"]
            elif r["status"] == "SUGESTAO":
                total_sugestao = r["total"]

        logger.info(
            f"Resumo execução {execucao_id} | AUTO: {total_auto} | SUGESTÕES: {total_sugestao}"
        )

        print("\n=== Resumo da Execução ===")
        print(f"Execução ID: {execucao_id}")
        print(f"Automáticos: {total_auto}")
        print(f"Sugestões: {total_sugestao}")

    except Exception:
        logger.exception(f"Erro ao gerar resumo da execução {execucao_id}")
        raise

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            logger.info("Conexão encerrada após resumo.")

# Utilizado para geração do relatório PDF
def gerar_resumo_execucao(execucao_id: int) -> dict:
    """
    Retorna resumo da execução:
    quantidade de AUTO e SUGESTAO.
    """

    from database.conexao import obter_conexao

    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)

    try:
        query = """
            SELECT 
                SUM(CASE WHEN status = 'AUTO' THEN 1 ELSE 0 END) AS auto,
                SUM(CASE WHEN status = 'SUGESTAO' THEN 1 ELSE 0 END) AS sugestoes
            FROM conciliacoes
            WHERE execucao_id = %s
        """

        cursor.execute(query, (execucao_id,))
        resultado = cursor.fetchone() or {}

        return {
            "auto": resultado.get("auto", 0) or 0,
            "sugestoes": resultado.get("sugestoes", 0) or 0
        }

    finally:
        cursor.close()
        conexao.close()