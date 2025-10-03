import fitz  # PyMuPDF
import pandas as pd
import re
import os

def extrair_dados_modelo_ge(caminho_pdf):

    try:
        doc = fitz.open(caminho_pdf)
        texto_completo = ""
        for pagina in doc:
            texto_completo += pagina.get_text("text", sort=True)
        doc.close()

        padrao_cabecalho_funcionario = r'(\d{5,}\s*-\s*.*?CPF:.*?\n)'
        partes = re.split(padrao_cabecalho_funcionario, texto_completo)

        if len(partes) <= 1:
            print("AVISO: Nenhum cabeçalho de funcionário válido foi encontrado.")
            return []

        lista_funcionarios = []
        
        for i in range(1, len(partes), 2):
            cabecalho = partes[i]
            corpo = partes[i+1] if (i+1) < len(partes) else ""
            bloco_completo = cabecalho + corpo
            
            dados_funcionario = {}

            # Extração dos campos já existentes
            if match := re.search(r'(\d{5,})\s*-\s*(.*?)\s*CPF:', cabecalho, re.DOTALL):
                dados_funcionario['Matricula'] = match.group(1).strip()
                dados_funcionario['Nome'] = match.group(2).strip().replace('\n', ' ')
            else:
                continue

            if match := re.search(r'Cargo:\s*(.*?)\s*(Função:|Departamento:)', bloco_completo, re.DOTALL):
                dados_funcionario['Cargo'] = match.group(1).strip()
            
            if match := re.search(r'Admissão:\s*([\d/]+)', bloco_completo):
                dados_funcionario['Admissão'] = match.group(1).strip()

            if match := re.search(r'Salário Base:\s*([\d.,]+)', bloco_completo):
                dados_funcionario['Salário Base'] = match.group(1).strip()

            if match := re.search(r'Total Bruto:\s*([\d.,]+)', bloco_completo):
                dados_funcionario['Total Bruto'] = match.group(1).strip()

            if match := re.search(r'Total de Descontos:\s*([\d.,]+)', bloco_completo):
                dados_funcionario['Total de Descontos'] = match.group(1).strip()

            if match := re.search(r'Total Salário Líquido:\s*([\d.,]+)', bloco_completo):
                dados_funcionario['Total Salário Líquido'] = match.group(1).strip()

            if match := re.search(r'9010 - INSS.* ([\d.,]+)', bloco_completo):
                dados_funcionario['INSS'] = match.group(1).strip()

            if match := re.search(r'Valor FGTS:\s*([\d.,]+)', bloco_completo):
                dados_funcionario['Valor FGTS'] = match.group(1).strip()

            if match := re.search(r'76 - IRRF.* ([\d.,]+)', bloco_completo):
                dados_funcionario['IRRF'] = match.group(1).strip()

            lista_funcionarios.append(dados_funcionario)

        return lista_funcionarios

    except Exception as e:
        print(f"Ocorreu um erro ao processar o PDF: {e}")
        return []


if __name__ == "__main__":
    caminho_do_arquivo = "Folha de Pagamento - TSE 1-2025.pdf"
    
    if not os.path.exists(caminho_do_arquivo):
        print(f"ERRO: O arquivo '{caminho_do_arquivo}' não foi encontrado na pasta.")
    else:
        dados = extrair_dados_modelo_ge_final_v4_2(caminho_do_arquivo)
        
        if dados:
            df = pd.DataFrame(dados)
            
            colunas_existentes = [col for col in [
                'Matricula', 'Nome', 'Cargo', 'Admissão', 'Salário Base',
                'Total Bruto', 'Total de Descontos', 'INSS', 'IRRF', 'Valor FGTS', 'Total Salário Líquido'
            ] if col in df.columns]
            
            df = df[colunas_existentes]
            caminho_saida = "folha_pagamento_ge_servicos.xlsx"
            df.to_excel(caminho_saida, index=False)
            
            print(f"SUCESSO! Planilha '{caminho_saida}' criada com {len(df)} registros")
        else:
            print("Nenhum dado foi extraído.")