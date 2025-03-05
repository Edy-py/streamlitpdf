import streamlit as st
from reportlab.pdfgen import canvas
from io import BytesIO

st.title(" Gerar Orçamento ")

parcela = None
# coletar info do usuário
nome = st.text_input("Nome do cliente:")
email = st.text_input("Email do cliente:")
descricao = st.text_area("Descrição do Serviço:")  # Usando text_area para aceitar mais texto
valor_serviço = st.text_input("Valor total:")
forma_pagamento = st.selectbox("Forma de pagamento:",["Pix/Dinheiro","Débito","Crédito à vista","Crédito parcelado"],index=None,placeholder="Selecione uma forma de pagamento")
if forma_pagamento == "Crédito parcelado":
    parcela = st.selectbox("Quantidade de parcelas",["2x","3x"],index=None,placeholder="Selecione o n° de parcelas")

if st.button("Gerar Pdf"):
    if nome.strip() or email.strip() or descricao.strip() or valor_serviço.strip():
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)

        # destacar titulo
        pdf.setFont("Helvetica-Bold",16)
        pdf.drawString(100,800, "EDSON PORTÕES")
        pdf.setFont("Helvetica",12)
        pdf.drawString(100,780, "CNPJ:")
        pdf.drawString(250,780, "Telefone:")
        pdf.setFont("Helvetica-Bold",12)
        pdf.drawString(100,760, "35.778.201/0001-07")
        pdf.drawString(250,760,"61 9 8560-1644")

        # inserir info user
        info_user = pdf.beginText(100,700)
        info_user.setTextOrigin(100,700)
        info_user.setLeading(14)
        
        info_user.setFont("Times-Bold",12)
        info_user.textOut("Nome: ")
        info_user.setFont("Times-Roman",12)
        info_user.textLine(nome)

        info_user.setFont("Times-Bold",12)
        info_user.textOut("Email do Cliente: ")
        info_user.setFont("Times-Roman",12)
        info_user.textLine(email)

        info_user.setFont("Times-Bold",12)
        info_user.textOut("Valor total do serviço ")
        info_user.setFont("Times-Roman",12)
        info_user.textLine(f"R${valor_serviço},00")
        
        info_user.setFont("Times-Bold",12)
        info_user.textOut("Forma de pagamento:")
        info_user.setFont("Times-Roman",12)

        if parcela is not None:
            info_user.textLine(f"{forma_pagamento}   N° de parcelas {parcela}")
        else:
            info_user.textLine(forma_pagamento)

        pdf.drawText(info_user)

        # Configurando o textObject para quebra automática de linha
        text_object = pdf.beginText(100, info_user.getY() - 14)  # Ajusta a posição para continuar abaixo
        text_object.setFont("Times-Roman", 12)
        text_object.setTextOrigin(100, info_user.getY() - 14)
        text_object.setLeading(14)  # Espaçamento entre linhas

        # Adicionando a descrição e quebrando a linha automaticamente
        text_object.setFont("Times-Bold",12)
        text_object.textOut("Descrição do Serviço: ")
        text_object.setFont("Times-Roman",12)

        # Wrap text to ensure it fits within the margin (adjust max_width as needed)
        max_width = 400  # Ajuste a largura máxima para caber dentro da página
        wrapped_text = []
        line = ''
        
        # Utiliza canvas.stringWidth() para calcular o comprimento do texto
        for word in descricao.split(' '):
            # Verifica se o texto da linha atual não ultrapassa a largura máxima
            if pdf.stringWidth(line + ' ' + word) < max_width:
                line += ' ' + word
            else:
                # Se ultrapassar, adiciona a linha ao wrapped_text e começa uma nova linha
                wrapped_text.append(line)
                line = word
        wrapped_text.append(line)  # Adiciona a última linha

        # Desenhando cada linha quebrada no PDF
        for line in wrapped_text:
            text_object.textLine(line)

        # Desenhando o texto no PDF
        pdf.drawText(text_object)

        # Finaliza o PDF
        pdf.save()
        buffer.seek(0)

        # Baixar o PDF gerado
        st.download_button("Baixar PDF", buffer, f"Orçamento_{nome}.pdf")
    else:
        st.warning("Preencha todos os dados antes de gerar o PDF.")
