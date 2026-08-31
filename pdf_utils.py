from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os

# Cores da Identidade Visual
COR_AZUL_ESCURO = colors.HexColor("#062356")
COR_AZUL_CLARO = colors.HexColor("#008FD3")
COR_AMARELO = colors.HexColor("#FFEA00")
COR_CINZA = colors.HexColor("#F0F0F0")
COR_TEXTO = colors.HexColor("#333333")

LOGO = "midia/logo_nova.png"

def formatar_moeda(valor):
    """Garante o formato brasileiro: 1.500,00"""
    return f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def desenhar_cabecalho_rodape(pdf, titulo_documento):
    largura, altura = A4
    
    # Cabeçalho
    pdf.setFillColor(COR_AZUL_ESCURO)
    pdf.rect(0, altura - 100, largura, 100, fill=True, stroke=False)
    pdf.setFillColor(COR_AMARELO)
    pdf.rect(0, altura - 105, largura, 5, fill=True, stroke=False)

    if os.path.exists(LOGO):
        try:
            pdf.drawImage(LOGO, 30, altura - 90, width=140, height=75, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
            
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(190, altura - 40, "EDSON PORTÕES")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(190, altura - 60, "FABRICAÇÃO, INSTALAÇÃO E MANUTENÇÃO")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(190, altura - 80, "CNPJ: 35.778.201/0001-07  |  Telefone: (61) 98560-1644")

    # Título
    pdf.setFillColor(COR_AZUL_CLARO)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(largura / 2, altura - 145, titulo_documento)
    
    # Rodapé
    pdf.setFillColor(COR_AZUL_ESCURO)
    pdf.rect(0, 0, largura, 40, fill=True, stroke=False)
    pdf.setFillColor(COR_AMARELO)
    pdf.rect(0, 40, largura, 3, fill=True, stroke=False)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(largura / 2, 15, "Edson Portões - Qualidade e segurança para sua casa")

def desenhar_texto_com_quebra(pdf, texto, x, y, max_width, fonte="Helvetica", tamanho=12, leading=16):
    pdf.setFillColor(COR_TEXTO)
    text_object = pdf.beginText(x, y)
    text_object.setFont(fonte, tamanho)
    text_object.setLeading(leading)

    linhas = texto.split('\n')
    for linha in linhas:
        palavras = linha.split(' ')
        linha_atual = ""
        for palavra in palavras:
            if pdf.stringWidth(linha_atual + " " + palavra, fonte, tamanho) < max_width:
                linha_atual += " " + palavra
            else:
                text_object.textLine(linha_atual.strip())
                linha_atual = palavra
        text_object.textLine(linha_atual.strip())
    
    pdf.drawText(text_object)
    return text_object.getY()