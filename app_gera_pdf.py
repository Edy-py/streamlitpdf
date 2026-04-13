import streamlit as st
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Gerar Orçamento Edson Portões", page_icon="📄", layout="centered")
st.title("Edson Portões - Gerar Orçamento")


parcela = None

# Inputs
nome = st.text_input("Nome do cliente:")
email = st.text_input("Email do cliente:")
descricao = st.text_area("Descrição do Serviço:")
valor_servico = st.text_input("Valor total:")
forma_pagamento = st.selectbox(
    "Forma de pagamento:",
    ["Pix/Dinheiro", "Débito", "Crédito à vista", "Crédito parcelado"],
    index=None,
    placeholder="Selecione uma forma de pagamento"
)

if forma_pagamento == "Crédito parcelado":
    parcela = st.selectbox(
        "Quantidade de parcelas",
        ["2x", "3x"],
        index=None,
        placeholder="Selecione o n° de parcelas"
    )

if st.button("Gerar Pdf"):
    if nome.strip() and descricao.strip() and valor_servico.strip():

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)

        # 🔝 HEADER
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(100, 800, "EDSON PORTÕES")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(100, 780, "CNPJ: 35.778.201/0001-07")
        pdf.drawString(300, 780, "Telefone: (61) 98560-1644")

        # Linha separadora
        pdf.line(100, 770, 500, 770)

        # 📅 Data
        pdf.setFont("Helvetica", 10)
        data_atual = datetime.now().strftime("%d/%m/%Y")
        pdf.drawString(400, 750, f"Data: {data_atual}")

        # 👤 CLIENTE
        y = 730
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100, y, "Cliente:")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(160, y, nome)

        y -= 20
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100, y, "Email:")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(150, y, email)

        # 💰 VALOR (DESTAQUE)
        y -= 40
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100, y, f"Valor Total: R$ {valor_servico}")

        # 💳 PAGAMENTO
        y -= 25
        pdf.setFont("Helvetica", 12)

        if parcela:
            pagamento_texto = f"{forma_pagamento} ({parcela})"
        else:
            pagamento_texto = forma_pagamento

        pdf.drawString(100, y, f"Forma de pagamento: {pagamento_texto}")

        # 📝 DESCRIÇÃO (COM CAIXA)
        y -= 40
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100, y, "Descrição do Serviço:")

        # Caixa
        box_y = y - 110
        pdf.rect(95, box_y, 420, 100)

        text_object = pdf.beginText(100, y - 20)
        text_object.setFont("Helvetica", 11)
        text_object.setLeading(14)

        # 🔥 CORREÇÃO DO ENTER
        linhas = descricao.split('\n')

        max_width = 380

        for linha in linhas:
            palavras = linha.split(' ')
            linha_atual = ""

            for palavra in palavras:
                if pdf.stringWidth(linha_atual + " " + palavra) < max_width:
                    linha_atual += " " + palavra
                else:
                    text_object.textLine(linha_atual.strip())
                    linha_atual = palavra

            text_object.textLine(linha_atual.strip())

        pdf.drawText(text_object)

        # ✍️ RODAPÉ
        pdf.line(100, 120, 500, 120)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(100, 100, "EDSON PORTÕES")
        pdf.drawString(100, 85, "Qualidade e segurança para sua casa")

        pdf.save()
        buffer.seek(0)

        st.download_button("Baixar PDF", buffer, f"Orcamento_{nome}.pdf")

    else:
        st.warning("Preencha todos os dados antes de gerar o PDF.")