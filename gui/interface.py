import sys
import os
from tkinter import Tk, Button, Text, ttk, END
from tkinter.scrolledtext import ScrolledText
from database.db_manager import salvar_boletim, carregar_boletins
from modules.pdf_analyzer import analisar_pdf

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def analisar_boletins():
    pasta = r"C:\BOUS"
    resultado_text.delete(1.0, END)
    if not os.path.exists(pasta):
        resultado_text.insert(END, f"Pasta '{pasta}' não encontrada.\n")
        return

    arquivos = [f for f in os.listdir(pasta) if f.endswith('.pdf')]
    if not arquivos:
        resultado_text.insert(END, "Nenhum arquivo PDF encontrado na pasta.\n")
        return

    for arquivo in arquivos:
        caminho_pdf = os.path.join(pasta, arquivo)
        ano, numero, natureza, local_da_ocorrencia = analisar_pdf(caminho_pdf)
        if ano and numero:
            resultado = salvar_boletim(ano, numero, natureza, local_da_ocorrencia)
            resultado_text.insert(END, f"Arquivo '{arquivo}': {resultado}\n")
        else:
            resultado_text.insert(END, f"Arquivo '{arquivo}' não é um Boletim de Ocorrência válido.\n")

def carregar_boletins_gui():
    for item in tabela.get_children():
        tabela.delete(item)
    boletins = carregar_boletins()
    for boletim in boletins:
        tabela.insert("", END, values=boletim)

def iniciar_interface():
    global resultado_text, tabela

    root = Tk()
    root.title("Project Kraken")
    root.geometry("900x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Aba 1: Analisador
    aba_analise = ttk.Frame(notebook)
    notebook.add(aba_analise, text="Analisador de Boletins")

    Button(aba_analise, text="Analisar Boletins", command=analisar_boletins).pack(pady=10)
    resultado_text = ScrolledText(aba_analise, wrap='word', height=20, width=100)
    resultado_text.pack(padx=10, pady=10)

    # Aba 2: Base de Dados
    aba_banco = ttk.Frame(notebook)
    notebook.add(aba_banco, text="Base de Dados")

    tabela = ttk.Treeview(aba_banco, columns=("Ano", "Número", "Natureza", "Local da ocorrência"), show="headings", height=20)
    tabela.heading("Ano", text="Ano")
    tabela.heading("Número", text="Número")
    tabela.heading("Natureza", text="Natureza")
    tabela.heading("Local da ocorrência", text="Local da ocorrência")
    tabela.pack(fill="both", padx=10, pady=10)

    Button(aba_banco, text="Atualizar Base de Dados", command=carregar_boletins_gui).pack(pady=10)

    root.mainloop()
