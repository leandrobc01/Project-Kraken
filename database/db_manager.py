import sqlite3

def criar_banco():
    conexao = sqlite3.connect("boletins.db")
    cursor = conexao.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS boletins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_boletim TEXT,
            ano_boletim INTEGER,
            natureza_chamada TEXT,
            endereco TEXT,
            numero TEXT,
            complemento TEXT,
            municipio_uf TEXT,
            bairro TEXT,
            UNIQUE(numero_boletim, ano_boletim)
        )
    ''')
    
    conexao.commit()
    conexao.close()
    print("Banco de dados criado com sucesso!")

# Criar banco ao executar o script
criar_banco()
