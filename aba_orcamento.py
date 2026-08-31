import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime
from db import carregar_json, salvar_json, ARQUIVO_CATALOGO
from pdf_utils import desenhar_cabecalho_rodape, formatar_moeda, COR_TEXTO, COR_CINZA, COR_AZUL_ESCURO, COR_AZUL_CLARO, COR_AMARELO, colors

def renderizar():
    col1, col2 = st.columns([2, 1])
    catalogo = carregar_json(ARQUIVO_CATALOGO)

    with col1:
        nome = st.text_input("Nome do cliente:", key="nome_orc")
        email = st.text_input("Email do cliente (opcional):", key="email_orc")
        
        forma_pagamento = st.selectbox(
            "Forma de pagamento sugerida:",
            ["Pix/Dinheiro", "Débito", "Crédito à vista", "Crédito parcelado"],
            index=None, key="pag_orc"
        )

        parcela = None
        if forma_pagamento == "Crédito parcelado":
            parcela = st.selectbox("Quantidade de parcelas", ["2x", "3x", "4x", "5x", "6x", "7x", "8x", "9x", "10x", "11x", "12x"], index=None, key="parc_orc")

        st.markdown("### Adicionar Serviços ao Orçamento")
        opcoes_servicos = ["-- Digitar Novo Serviço --"] + list(catalogo.keys())
        servico_selecionado = st.selectbox("Selecione do Catálogo ou crie um novo:", opcoes_servicos, key="sel_serv_orc")
        
        if servico_selecionado == "-- Digitar Novo Serviço --":
            nome_serv = st.text_input("Nome do Serviço:", key="nome_serv_orc")
            valor_serv = st.number_input("Valor (R$):", min_value=0.0, step=50.0, format="%.2f", key="val_serv_orc")
        else:
            nome_serv = servico_selecionado
            valor_serv = st.number_input("Valor (R$) - Editável:", value=float(catalogo[servico_selecionado]), step=50.0, format="%.2f", key="val_serv_edit_orc")
            
        if st.button("➕ Adicionar ao Orçamento", type="secondary"):
            if nome_serv:
                st.session_state.itens_orcamento.append({"servico": nome_serv, "valor": valor_serv})
                st.rerun()

    with col2:
        st.markdown("### Resumo do Orçamento")
        total_orcamento = sum(item["valor"] for item in st.session_state.itens_orcamento)
        
        if len(st.session_state.itens_orcamento) > 0:
            for item in st.session_state.itens_orcamento:
                st.write(f"- {item['servico']}: **R$ {formatar_moeda(item['valor'])}**")
            st.markdown(f"**Total: R$ {formatar_moeda(total_orcamento)}**")
            
            if st.button("Limpar Lista", key="limpar_orc"):
                st.session_state.itens_orcamento = []
                st.rerun()
        else:
            st.warning("Nenhum serviço adicionado.")

    st.divider()

    if st.button("Gerar Orçamento em PDF", key="btn_orc", type="primary", use_container_width=True):
        if nome.strip() and len(st.session_state.itens_orcamento) > 0:
            
            # Atualiza o catálogo com novos serviços orçados
            for item in st.session_state.itens_orcamento:
                catalogo[item["servico"]] = item["valor"]
            salvar_json(catalogo, ARQUIVO_CATALOGO)

            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=A4)
            largura, altura = A4

            desenhar_cabecalho_rodape(pdf, "ORÇAMENTO")

            pdf.setFillColor(COR_TEXTO)
            pdf.setFont("Helvetica", 10)
            data_atual = datetime.now().strftime("%d/%m/%Y")
            pdf.drawString(largura - 150, altura - 130, f"Data: {data_atual}")

            # Dados do Cliente
            y_cliente = altura - 200
            pdf.setFillColor(COR_CINZA)
            pdf.setStrokeColor(COR_AZUL_CLARO)
            pdf.setLineWidth(1)
            pdf.roundRect(40, y_cliente, largura - 80, 50, 5, fill=True, stroke=True)
            
            pdf.setFillColor(COR_AZUL_ESCURO)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(50, y_cliente + 30, "Dados do Cliente:")
            pdf.setFillColor(COR_TEXTO)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(50, y_cliente + 10, f"Nome: {nome}")
            pdf.drawString(300, y_cliente + 10, f"Email: {email if email else 'Não informado'}")

            # Tabela de Serviços
            y_tabela = y_cliente - 40
            pdf.setFillColor(COR_AZUL_ESCURO)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(50, y_tabela, "Serviços Orçados")
            pdf.drawString(largura - 150, y_tabela, "Valor")
            pdf.line(50, y_tabela - 5, largura - 50, y_tabela - 5)
            
            y_tabela -= 25
            pdf.setFillColor(COR_TEXTO)
            pdf.setFont("Helvetica", 11)
            for item in st.session_state.itens_orcamento:
                pdf.drawString(50, y_tabela, f"• {item['servico']}")
                pdf.drawString(largura - 150, y_tabela, f"R$ {formatar_moeda(item['valor'])}")
                pdf.setStrokeColor(COR_CINZA)
                pdf.setLineWidth(0.5)
                pdf.line(50, y_tabela - 5, largura - 50, y_tabela - 5)
                y_tabela -= 20

            # Condições de Pagamento e Total
            y_valor = y_tabela - 50
            pdf.setFillColor(COR_AZUL_ESCURO)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(50, y_valor + 20, "Condições de Pagamento:")
            pdf.setFillColor(COR_TEXTO)
            pdf.setFont("Helvetica", 11)
            pagamento_texto = f"{forma_pagamento} ({parcela})" if parcela else (forma_pagamento if forma_pagamento else "A combinar")
            pdf.drawString(50, y_valor, pagamento_texto)

            pdf.setFillColor(COR_AZUL_ESCURO)
            pdf.roundRect(largura - 250, y_valor - 20, 200, 60, 5, fill=True, stroke=False)
            pdf.setFillColor(colors.white)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(largura - 235, y_valor + 20, "Valor Total:")
            pdf.setFillColor(COR_AMARELO)
            pdf.setFont("Helvetica-Bold", 18)
            pdf.drawCentredString(largura - 150, y_valor - 5, f"R$ {formatar_moeda(total_orcamento)}")

            # Validade
            pdf.setFillColor(COR_TEXTO)
            pdf.setFont("Helvetica-Oblique", 10)
            pdf.drawCentredString(largura / 2, y_valor - 80, "Este orçamento é válido por 15 dias a partir da data de emissão.")

            pdf.save()
            buffer.seek(0)
            st.success("Orçamento gerado!")
            st.download_button("Baixar Orçamento PDF", buffer, f"Orcamento_{nome}.pdf", key="dl_orc_final")
        else:
            st.warning("Preencha o Nome e adicione pelo menos um serviço.")