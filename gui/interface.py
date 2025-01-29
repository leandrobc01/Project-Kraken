import tkinter as tk
from tkinter import ttk
from pathlib import Path  # 🔹 Correção adicionada
from modules.pdf_analyzer import analisar_pdfs
from database.db_manager import inicializar_banco

def iniciar_interface():
    inicializar_banco()

    janela = tk.Tk()
    janela.title("Analisador de BOUs")

    abas = ttk.Notebook(janela)

    aba_processamento = ttk.Frame(abas)
    abas.add(aba_processamento, text="Processamento")

    aba_base_dados = ttk.Frame(abas)
    abas.add(aba_base_dados, text="Base de Dados")

    abas.pack(expand=1, fill="both")

    # Área de logs
    log_text = tk.Text(aba_processamento, height=15, width=80)
    log_text.pack()

    def processar():
        log_text.insert(tk.END, "Iniciando processamento...\n")
        caminho_pasta = Path("C:/BOUS")  # 🔹 Agora o Path foi importado corretamente
        analisar_pdfs(caminho_pasta)
        log_text.insert(tk.END, "Processamento concluído.\n")

    botao_processar = tk.Button(aba_processamento, text="Processar PDFs", command=processar)
    botao_processar.pack()

    botao_atualizar = tk.Button(aba_base_dados, text="Atualizar Base de Dados")
    botao_atualizar.pack()

    janela.mainloop()
