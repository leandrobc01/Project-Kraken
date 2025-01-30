import fitz  # PyMuPDF

print(fitz.__doc__)

def extrair_dados_pdf(caminho_pdf):
    with fitz.open(caminho_pdf) as doc:
        primeira_pagina = doc[0]  # Pegamos a primeira página
        texto = primeira_pagina.get_text("text")  # Extraímos o texto
    
    # Dicionário para armazenar os dados extraídos
    dados_extraidos = {}
    
    # Extração usando palavras-chave
    campos = [
        ("Número do Boletim", r"B\.O\. N: (\d+/\d+)"),
        ("Natureza da Chamada", r"NATUREZA DA CHAMADA:\s*(.*)"),
        ("Endereço", r"ENDEREÇO:\s*(.*)"),
        ("Número", r"NÚMERO:\s*(\d+)"),
        ("Complemento", r"COMPLEMENTO:\s*(.*)"),
        ("Município/UF", r"MUNICÍPIO/UF:\s*(.*)"),
        ("Bairro", r"BAIRRO:\s*(.*)")
    ]

    
    for campo, regex in campos:
        import re
        match = re.search(regex, texto)
        if match:
            dados_extraidos[campo] = match.group(1).strip()
    
    return dados_extraidos

# Exemplo de uso
dados = extrair_dados_pdf("BOU_2015_1215226.pdf")
print(dados)