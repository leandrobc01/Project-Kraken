import sys
import os
import re
from PyPDF2 import PdfReader

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def analisar_pdf(caminho_pdf):
    try:
        reader = PdfReader(caminho_pdf)
        texto_pagina1 = reader.pages[0].extract_text()

        # Extrair ano e número
        match_boletim = re.search(r"B\.O\. N: (\d{4})/(\d+)", texto_pagina1)
        if match_boletim:
            ano = int(match_boletim.group(1))
            numero = int(match_boletim.group(2))
        else:
            ano, numero = None, None

        # Extrair natureza
        match_natureza = re.search(r"NATUREZA DA CHAMADA:\s*(.*)", texto_pagina1)
        natureza = match_natureza.group(1).strip() if match_natureza else "Não informada"

        # Extrair endereço
        endereco_match = re.search(r"ENDEREÇO:\s*(.*)", texto_pagina1)
        numero_match = re.search(r"NÚMERO:\s*(.*)", texto_pagina1)
        complemento_match = re.search(r"COMPLEMENTO:\s*(.*)", texto_pagina1)
        bairro_match = re.search(r"BAIRRO:\s*(.*)", texto_pagina1)
        municipio_match = re.search(r"MUNICÍPIO/UF:\s*(.*)", texto_pagina1)

        # Garantir que os valores sejam extraídos como strings e tratados
        endereco = endereco_match.group(1).strip() if endereco_match else "Não informado"
        numero = numero_match.group(1).strip() if numero_match else "Não informado"
        complemento = complemento_match.group(1).strip() if complemento_match else ""
        bairro = bairro_match.group(1).strip() if bairro_match else "Não informado"
        municipio = municipio_match.group(1).strip() if municipio_match else "Não informado"

        # Construir o local da ocorrência
        local_da_ocorrencia = ", ".join(filter(None, [endereco, numero, complemento, bairro, municipio]))

        return ano, numero, natureza, local_da_ocorrencia
    except Exception as e:
        print(f"Erro ao analisar o PDF {caminho_pdf}: {e}")
        return None, None, None, None
