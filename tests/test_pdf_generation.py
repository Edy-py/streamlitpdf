import sys
import os
import io

# Adiciona o diretório atual ao path
sys.path.append(os.getcwd())

from execution.pdf_generator import gerar_pdf_orcamento

def test_geracao_pdf():
    print("Iniciando teste de geração de PDF...")
    try:
        pdf_buffer = gerar_pdf_orcamento(
            nome="Teste Cliente",
            email="teste@email.com",
            descricao="Serviço de teste com descrição longa para verificar a quebra de linha automática implementada no módulo.",
            valor="1500,00",
            forma_pagamento="Pix/Dinheiro"
        )
        
        if isinstance(pdf_buffer, io.BytesIO):
             print("SUCESSO: PDF gerado e retornado como BytesIO.")
             size = pdf_buffer.getbuffer().nbytes
             print(f"Tamanho do PDF: {size} bytes")
             if size > 0:
                 print("SUCESSO: O arquivo não está vazio.")
             else:
                 print("FALHA: O arquivo PDF está vazio.")
        else:
            print("FALHA: O retorno não é um objeto BytesIO.")
            
    except Exception as e:
        print(f"ERRO durante a geração do PDF: {e}")

if __name__ == "__main__":
    test_geracao_pdf()
