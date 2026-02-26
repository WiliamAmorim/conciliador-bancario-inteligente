import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)


COLUNAS_OBRIGATORIAS = ["data", "descricao", "valor"]


def _validar_dataframe(df, caminho):
    """
    Valida se o DataFrame possui as colunas obrigatórias.
    """
    colunas_faltantes = [
        col for col in COLUNAS_OBRIGATORIAS if col not in df.columns
    ]

    if colunas_faltantes:
        raise ValueError(
            f"Arquivo {caminho} não possui colunas obrigatórias: {colunas_faltantes}"
        )


def _padronizar_dataframe(df, caminho, origem):
    """
    Padroniza colunas, valida estrutura e converte tipos.
    """
    df.columns = df.columns.str.lower().str.strip()

    _validar_dataframe(df, caminho)

    df["data"] = pd.to_datetime(df["data"], errors="raise")
    df["valor"] = pd.to_numeric(df["valor"], errors="raise")

    df["origem"] = origem

    return df


def carregar_extrato(caminho):

    try:
        logger.info(f"Iniciando leitura do extrato: {caminho}")

        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        df = pd.read_csv(caminho)

        df = _padronizar_dataframe(df, caminho, "extrato")

        logger.info(f"Extrato carregado com sucesso | Registros: {len(df)}")

        return df

    except Exception:
        logger.exception(f"Erro ao carregar extrato: {caminho}")
        raise


def carregar_controle(caminho):

    try:
        logger.info(f"Iniciando leitura do controle: {caminho}")

        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        df = pd.read_excel(caminho)

        df = _padronizar_dataframe(df, caminho, "controle")

        logger.info(f"Controle carregado com sucesso | Registros: {len(df)}")

        return df

    except Exception:
        logger.exception(f"Erro ao carregar controle: {caminho}")
        raise