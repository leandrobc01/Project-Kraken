from gui.interface import iniciar_interface
from database.db_manager import inicializar_banco
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Inicializar banco de dados
    inicializar_banco()
    # Iniciar a interface gráfica
    iniciar_interface()
