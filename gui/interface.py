import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.pdf_analyzer import extrair_dados_pdf, inserir_dados_no_banco

def selecionar_arquivos():
    arquivos = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    for arquivo in arquivos:
        dados = extrair_dados_pdf(arquivo)
        inserir_dados_no_banco(dados)
    atualizar_lista()
    messagebox.showinfo("Sucesso", "Processamento concluído!")

def atualizar_lista():
    conexao = sqlite3.connect("boletins.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT numero_boletim, ano_boletim, natureza_chamada FROM boletins")
    registros = cursor.fetchall()
    conexao.close()
    
    lista_boletins.delete(0, tk.END)
    for registro in registros:
        lista_boletins.insert(tk.END, f"{registro[0]}/{registro[1]} - {registro[2]}")

def criar_interface():
    global lista_boletins
    root = tk.Tk()
    root.title("Kraken - Análise Criminal")
    root.geometry("600x400")
    
    btn_selecionar = tk.Button(root, text="Selecionar PDFs", command=selecionar_arquivos)
    btn_selecionar.pack(pady=10)
    
    btn_atualizar = tk.Button(root, text="Atualizar Base de Dados", command=atualizar_lista)
    btn_atualizar.pack(pady=5)
    
    lista_boletins = tk.Listbox(root, width=80, height=15)
    lista_boletins.pack(pady=10)
    
    atualizar_lista()
    root.mainloop()

if __name__ == "__main__":
    criar_interface()