import sqlite3
import os

# Caminho do banco de dados
DB_PATH = "boletins.db"


def inicializar_banco():
    """
    Inicializa o banco de dados e garante que a tabela 'boletins' 
    está configurada corretamente com todas as colunas necessárias.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Criar tabela, se ainda não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS boletins (
            ano INTEGER,
            numero INTEGER,
            natureza TEXT,
            local_da_ocorrencia TEXT,
            PRIMARY KEY (ano, numero)
        )
    """)

    # Garantir que as colunas estejam presentes na tabela
    cursor.execute("PRAGMA table_info(boletins)")
    colunas_existentes = [col[1] for col in cursor.fetchall()]

    # Adicionar colunas, se necessário
    if "natureza" not in colunas_existentes:
        cursor.execute("ALTER TABLE boletins ADD COLUMN natureza TEXT")
    if "local_da_ocorrencia" not in colunas_existentes:
        cursor.execute("ALTER TABLE boletins ADD COLUMN local_da_ocorrencia TEXT")

    conn.commit()
    conn.close()


def salvar_boletim(ano, numero, natureza, local_da_ocorrencia):
    """
    Salva os dados de um boletim de ocorrência no banco de dados.

    Args:
        ano (int): Ano do boletim.
        numero (int): Número do boletim.
        natureza (str): Natureza da chamada.
        local_da_ocorrencia (str): Local da ocorrência no formato concatenado.

    Returns:
        str: Mensagem de sucesso ou erro.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO boletins (ano, numero, natureza, local_da_ocorrencia)
            VALUES (?, ?, ?, ?)
        """, (ano, numero, natureza, local_da_ocorrencia))

        conn.commit()
        conn.close()
        return f"Boletim {numero}/{ano} salvo com sucesso."

    except sqlite3.IntegrityError:
        return f"Erro: O boletim {numero}/{ano} já existe no banco de dados."
    except Exception as e:
        return f"Erro ao salvar o boletim: {str(e)}"


def listar_boletins():
    """
    Lista todos os boletins registrados no banco de dados.

    Returns:
        list: Lista de boletins no formato [(ano, numero, natureza, local_da_ocorrencia), ...].
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT ano, numero, natureza, local_da_ocorrencia FROM boletins")
        boletins = cursor.fetchall()

        conn.close()
        return boletins

    except Exception as e:
        return f"Erro ao listar boletins: {str(e)}"


def excluir_boletim(ano, numero):
    """
    Exclui um boletim de ocorrência do banco de dados.

    Args:
        ano (int): Ano do boletim.
        numero (int): Número do boletim.

    Returns:
        str: Mensagem de sucesso ou erro.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM boletins WHERE ano = ? AND numero = ?", (ano, numero))

        if cursor.rowcount == 0:
            return f"Boletim {numero}/{ano} não encontrado."

        conn.commit()
        conn.close()
        return f"Boletim {numero}/{ano} excluído com sucesso."

    except Exception as e:
        return f"Erro ao excluir o boletim: {str(e)}"


def buscar_boletim(ano, numero):
    """
    Busca um boletim específico no banco de dados.

    Args:
        ano (int): Ano do boletim.
        numero (int): Número do boletim.

    Returns:
        tuple or str: Boletim encontrado no formato (ano, numero, natureza, local_da_ocorrencia) ou mensagem de erro.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ano, numero, natureza, local_da_ocorrencia
            FROM boletins
            WHERE ano = ? AND numero = ?
        """, (ano, numero))

        boletim = cursor.fetchone()

        conn.close()
        if boletim:
            return boletim
        else:
            return f"Boletim {numero}/{ano} não encontrado."

    except Exception as e:
        return f"Erro ao buscar boletim: {str(e)}"

def carregar_boletins():
    """
    Carrega todos os boletins salvos no banco de dados.

    Returns:
        list: Lista de boletins no formato [(ano, numero, natureza, local_da_ocorrencia), ...].
    """
    return listar_boletins()  # Reutilizando a função já existente


# Inicializar banco ao importar o módulo
if not os.path.exists(DB_PATH):
    inicializar_banco()
