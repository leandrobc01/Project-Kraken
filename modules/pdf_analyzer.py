import pdfplumber
import re
import requests
from database.db_manager import salvar_boletim

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

def obter_coordenadas(endereco_formatado):
    try:
        params = {"q": endereco_formatado, "format": "json"}
        resposta = requests.get(NOMINATIM_URL, params=params, timeout=10)
        dados = resposta.json()

        if dados and isinstance(dados, list) and len(dados) > 0:
            latitude = dados[0]["lat"]
            longitude = dados[0]["lon"]
            return latitude, longitude
        else:
            print(f"Endereço não encontrado: {endereco_formatado}")
            return None, None
    except Exception as e:
        print(f"Erro ao obter coordenadas: {e}")
        return None, None

def analisar_pdfs(caminho_pasta):
    for arquivo in caminho_pasta.glob("*.pdf"):
        try:
            with pdfplumber.open(arquivo) as pdf:
                texto = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

            endereco_match = re.search(r"ENDEREÇO:\s*(.*)", texto)
            numero_match = re.search(r"NÚMERO:\s*(\d+)", texto)
            bairro_match = re.search(r"BAIRRO:\s*(.*)", texto)
            municipio_match = re.search(r"MUNICÍPIO/UF:\s*([\w\s]+)-?\s*([A-Z]{2})?", texto)
            complemento_match = re.search(r"COMPLEMENTO:\s*(.*)", texto)

            endereco = endereco_match.group(1).strip() if endereco_match else ""
            numero = numero_match.group(1).strip() if numero_match else ""
            bairro = bairro_match.group(1).strip() if bairro_match else ""
            municipio = municipio_match.group(1).strip() if municipio_match else ""
            uf = municipio_match.group(2).strip() if municipio_match and municipio_match.group(2) else "PR"
            complemento = complemento_match.group(1).strip() if complemento_match and complemento_match.group(1) else ""

            # Formatar o endereço corretamente
            endereco_formatado = f"{endereco}, {numero}, {bairro}, {municipio} - {uf}"

            latitude, longitude = obter_coordenadas(endereco_formatado)

            salvar_boletim(endereco, numero, bairro, f"{municipio} - {uf}", complemento, latitude, longitude)
            
            print(f"Processado com sucesso: {arquivo.name}")

        except Exception as e:
            print(f"Erro ao processar {arquivo.name}: {e}")
