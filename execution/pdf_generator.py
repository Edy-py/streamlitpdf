import io
from typing import Optional
from reportlab.pdfgen import canvas


def gerar_pdf_orcamento(
    nome: str,
    email: str,
    descricao: str,
    valor: str,
    forma_pagamento: str,
    parcelas: Optional[str] = None
) -> io.BytesIO:
    """
    Gera um arquivo PDF de orçamento com os dados fornecidos.

    :param nome: Nome do cliente.
    :type nome: str
    :param email: Email do cliente.
    :type email: str
    :param descricao: Descrição do serviço a ser realizado.
    :type descricao: str
    :param valor: Valor total do serviço.
    :type valor: str
    :param forma_pagamento: Forma de pagamento escolhida.
    :type forma_pagamento: str
    :param parcelas: Quantidade de parcelas (opcional), ex: "2x".
    :type parcelas: Optional[str]
    :return: Um objeto BytesIO contendo os dados do PDF gerado.
    :rtype: io.BytesIO
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    # Destacar título
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 800, "EDSON PORTÕES")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 780, "CNPJ:")
    pdf.drawString(250, 780, "Telefone:")
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, 760, "35.778.201/0001-07")
    pdf.drawString(250, 760, "61 9 8560-1644")

    # Inserir informações do usuário
    info_user = pdf.beginText(100, 700)
    info_user.setTextOrigin(100, 700)
    info_user.setLeading(14)

    info_user.setFont("Times-Bold", 12)
    info_user.textOut("Nome: ")
    info_user.setFont("Times-Roman", 12)
    info_user.textLine(nome)

    info_user.setFont("Times-Bold", 12)
    info_user.textOut("Email do Cliente: ")
    info_user.setFont("Times-Roman", 12)
    info_user.textLine(email)

    info_user.setFont("Times-Bold", 12)
    info_user.textOut("Valor total do serviço ")
    info_user.setFont("Times-Roman", 12)
    info_user.textLine(f"R${valor}")

    info_user.setFont("Times-Bold", 12)
    info_user.textOut("Forma de pagamento:")
    info_user.setFont("Times-Roman", 12)

    if parcelas is not None:
        info_user.textLine(f"{forma_pagamento}   N° de parcelas {parcelas}")
    else:
        info_user.textLine(forma_pagamento)

    pdf.drawText(info_user)

    # Configurando o textObject para quebra automática de linha
    # Ajusta a posição para continuar abaixo
    text_object = pdf.beginText(100, info_user.getY() - 14)
    text_object.setFont("Times-Roman", 12)
    text_object.setTextOrigin(100, info_user.getY() - 14)
    text_object.setLeading(14)  # Espaçamento entre linhas

    # Adicionando a descrição e quebrando a linha automaticamente
    text_object.setFont("Times-Bold", 12)
    text_object.textOut("Descrição do Serviço: ")
    text_object.setFont("Times-Roman", 12)

    # Wrap text to ensure it fits within the margin
    max_width = 400
    wrapped_text = []
    line = ''

    # Utiliza canvas.stringWidth() para calcular o comprimento do texto
    for word in descricao.split(' '):
        # Verifica se o texto da linha atual não ultrapassa a largura máxima
        if pdf.stringWidth(line + ' ' + word) < max_width:
            line += ' ' + word
        else:
            # Se ultrapassar, adiciona a linha ao wrapped_text e começa nova
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
    return buffer
