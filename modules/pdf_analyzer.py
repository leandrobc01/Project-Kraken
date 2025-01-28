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
        ano, numero = (int(match_boletim.group(1)), int(match_boletim.group(2))) if match_boletim else (None, None)

        # Extrair natureza
        match_natureza = re.search(r"NATUREZA DA CHAMADA:\s*(.*)", texto_pagina1)
        natureza = match_natureza.group(1).strip() if match_natureza else "Não informada"

        # Extrair endereço
        endereco = re.search(r"ENDEREÇO:\s*(.*)", texto_pagina1)
        numero = re.search(r"NÚMERO:\s*(.*)", texto_pagina1)
        complemento = re.search(r"COMPLEMENTO:\s*(.*)", texto_pagina1)
        bairro = re.search(r"BAIRRO:\s*(.*)", texto_pagina1)
        municipio = re.search(r"MUNICÍPIO/UF:\s*(.*)", texto_pagina1)

        local_da_ocorrencia = ", ".join(filter(None, [
            endereco.group(1).strip() if endereco else "Não informado",
            numero.group(1).strip() if numero else "Não informado",
            complemento.group(1).strip() if complemento else "",
            bairro.group(1).strip() if bairro else "Não informado",
            municipio.group(1).strip() if municipio else "Não informado"
        ]))

        return ano, numero, natureza, local_da_ocorrencia
    except Exception as e:
        return None, None, None, None
