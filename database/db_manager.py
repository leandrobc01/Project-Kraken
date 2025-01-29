import sqlite3

BANCO_DADOS = "boletins.db"

def inicializar_banco():
    conexao = sqlite3.connect(BANCO_DADOS)
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS boletins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endereco TEXT,
            numero TEXT,
            bairro TEXT,
            municipio TEXT,
            complemento TEXT,
            latitude TEXT,
            longitude TEXT
        )
    """)
    
    conexao.commit()
    conexao.close()

def salvar_boletim(endereco, numero, bairro, municipio, complemento, latitude, longitude):
    try:
        conexao = sqlite3.connect(BANCO_DADOS)
        cursor = conexao.cursor()
        
        cursor.execute("""
            INSERT INTO boletins (endereco, numero, bairro, municipio, complemento, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (endereco, numero, bairro, municipio, complemento, latitude, longitude))
        
        conexao.commit()
        conexao.close()
    except Exception as e:
        print(f"Erro ao salvar boletim: {e}")
