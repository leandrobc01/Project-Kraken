import os
import re
import sqlite3
from tkinter import Tk, Text, Button, END, ttk
from tkinter.scrolledtext import ScrolledText
from PyPDF2 import PdfReader

# Configuração do banco de dados
def inicializar_banco():
    conn = sqlite3.connect("boletins.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS boletins (
            ano INTEGER,
            numero INTEGER,
            PRIMARY KEY (ano, numero)
        )
    """)
    conn.commit()
    conn.close()

# Função para salvar no banco de dados
def salvar_boletim(ano, numero):
    conn = sqlite3.connect("boletins.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO boletins (ano, numero) VALUES (?, ?)", (ano, numero))
        conn.commit()
        resultado_text.insert(END, f"Boletim {ano}/{numero} salvo no banco de dados.\n")
    except sqlite3.IntegrityError:
        resultado_text.insert(END, f"Boletim {ano}/{numero} já está registrado no banco de dados.\n")
    finally:
        conn.close()

# Função para analisar os boletins
def analisar_boletins():
    pasta = r"C:\BOUS"  # Caminho fixo da pasta (você pode permitir escolher depois)
    resultado_text.delete(1.0, END)  # Limpar o campo de texto
    
    # Verifica se a pasta existe
    if not os.path.exists(pasta):
        resultado_text.insert(END, f"Pasta '{pasta}' não encontrada.\n")
        return

    resultado_text.insert(END, f"Pasta '{pasta}' encontrada.\n")

    # Lista os arquivos PDF na pasta
    arquivos = [f for f in os.listdir(pasta) if f.endswith('.pdf')]
    if not arquivos:
        resultado_text.insert(END, "Nenhum arquivo PDF encontrado na pasta.\n")
        return

    resultado_text.insert(END, f"{len(arquivos)} arquivo(s) PDF encontrado(s): {arquivos}\n")

    # Processar cada arquivo PDF
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(pasta, arquivo)
        try:
            # Abrir e ler o conteúdo do PDF
            reader = PdfReader(caminho_arquivo)
            texto_pagina1 = reader.pages[0].extract_text()

            # Procurar o padrão do Boletim de Ocorrência
            match = re.search(r"B\.O\. N: (\d{4})/(\d+)", texto_pagina1)
            if match:
                ano, numero = match.groups()
                ano = int(ano)
                numero = int(numero)
                resultado_text.insert(END, f"Arquivo '{arquivo}' é um Boletim de Ocorrência válido.\n")
                resultado_text.insert(END, f" - Ano: {ano}\n")
                resultado_text.insert(END, f" - Número: {numero}\n")
                # Salvar no banco de dados
                salvar_boletim(ano, numero)
            else:
                resultado_text.insert(END, f"Arquivo '{arquivo}' não é um Boletim de Ocorrência válido.\n")
        except Exception as e:
            resultado_text.insert(END, f"Erro ao processar o arquivo '{arquivo}': {e}\n")

# Função para exibir boletins salvos
def carregar_boletins():
    for item in tabela.get_children():
        tabela.delete(item)  # Limpar tabela
    conn = sqlite3.connect("boletins.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ano, numero FROM boletins ORDER BY ano, numero")
    boletins = cursor.fetchall()
    conn.close()

    # Adicionar boletins à tabela
    for boletim in boletins:
        tabela.insert("", END, values=boletim)

# Criação da interface gráfica
root = Tk()
root.title("Analisador de Boletins de Ocorrência")
root.geometry("700x500")

# Sistema de abas
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Aba 1: Analisador de Boletins
aba_analise = ttk.Frame(notebook)
notebook.add(aba_analise, text="Analisador de Boletins")

executar_btn = Button(aba_analise, text="Analisar Boletins", command=analisar_boletins)
executar_btn.pack(pady=10)

resultado_text = ScrolledText(aba_analise, wrap='word', height=20, width=80)
resultado_text.pack(padx=10, pady=10)

# Aba 2: Acesso ao Banco de Dados
aba_banco = ttk.Frame(notebook)
notebook.add(aba_banco, text="Base de Dados")

tabela = ttk.Treeview(aba_banco, columns=("Ano", "Número"), show="headings", height=20)
tabela.heading("Ano", text="Ano")
tabela.heading("Número", text="Número")
tabela.column("Ano", width=100, anchor="center")
tabela.column("Número", width=150, anchor="center")
tabela.pack(fill="both", padx=10, pady=10)

# Botão para atualizar a tabela
atualizar_btn = Button(aba_banco, text="Atualizar Base de Dados", command=carregar_boletins)
atualizar_btn.pack(pady=1)

# Inicializar o banco de dados
inicializar_banco()

# Iniciar o loop da interface
root.mainloop()
