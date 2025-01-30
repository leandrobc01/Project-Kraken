import sys
import os
import fitz  # PyMuPDF
import sqlite3

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db_manager import criar_banco

def extrair_dados_pdf(caminho_pdf):
    with fitz.open(caminho_pdf) as doc:
        primeira_pagina = doc[0]  # Pegamos a primeira página
        texto = primeira_pagina.get_text("text")  # Extraímos o texto
    
    # Dicionário para armazenar os dados extraídos
    dados_extraidos = {}
    
    # Extração usando palavras-chave
    import re
    campos = [
        ("numero_boletim", r"B\.O\. N: (\d+)/(\d+)", True),
        ("natureza_chamada", r"NATUREZA DA CHAMADA:\s*(.*)", False),
        ("endereco", r"ENDEREÇO:\s*(.*)", False),
        ("numero", r"NÚMERO:\s*(\d+)", False),
        ("complemento", r"COMPLEMENTO:\s*(.*)", False),
        ("municipio_uf", r"MUNICÍPIO/UF:\s*(.*)", False),
        ("bairro", r"BAIRRO:\s*(.*)", False)
    ]
    
    for campo, regex, is_boletim in campos:
        match = re.search(regex, texto)
        if match:
            dados_extraidos[campo] = match.group(1).strip()
            if is_boletim:
                dados_extraidos["ano_boletim"] = match.group(2)  # Extrai o ano separado
    
    return dados_extraidos

def inserir_dados_no_banco(dados):
    conexao = sqlite3.connect("boletins.db")
    cursor = conexao.cursor()
    
    cursor.execute('''
        INSERT INTO boletins (
            numero_boletim, ano_boletim, natureza_chamada, endereco, numero, complemento, municipio_uf, bairro
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        dados.get("numero_boletim"),
        dados.get("ano_boletim"),
        dados.get("natureza_chamada"),
        dados.get("endereco"),
        dados.get("numero"),
        dados.get("complemento"),
        dados.get("municipio_uf"),
        dados.get("bairro")
    ))
    
    conexao.commit()
    conexao.close()
    print("Dados inseridos com sucesso!")

# Exemplo de uso
dados = extrair_dados_pdf("BOU_2015_1215226.pdf")
inserir_dados_no_banco(dados)