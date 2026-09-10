import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from db import carregar_json, salvar_json, ARQUIVO_CATALOGO, ARQUIVO_HISTORICO
from pdf_utils import desenhar_cabecalho_rodape, desenhar_texto_com_quebra, formatar_moeda, COR_TEXTO, COR_CINZA, COR_AZUL_ESCURO, COR_AZUL_CLARO

def renderizar():
    col1, col2 = st.columns([2, 1])
    
    catalogo = carregar_json(ARQUIVO_CATALOGO)
    historico = carregar_json(ARQUIVO_HISTORICO)
    if not isinstance(historico, list): historico = []

    with col1:
        nome_pagador = st.text_input("Recebemos de (Nome do cliente):", key="nome_rec")
        data_recibo = st.date_input("Data do recibo:", format="DD/MM/YYYY")
        
        st.markdown("### Adicionar Serviços")
        opcoes_servicos = ["-- Digitar Novo Serviço --"] + list(catalogo.keys())
        servico_selecionado = st.selectbox("Selecione do Histórico ou crie um novo:", opcoes_servicos)
        
        if servico_selecionado == "-- Digitar Novo Serviço --":
            nome_serv = st.text_input("Nome do Serviço:")
            valor_serv = st.number_input("Valor (R$):", min_value=0.0, step=50.0, format="%.2f")
        else:
            nome_serv = servico_selecionado
            valor_serv = st.number_input("Valor (R$) - Editável:", value=float(catalogo[servico_selecionado]), step=50.0, format="%.2f")
            
        if st.button("➕ Adicionar ao Recibo", type="secondary"):
            if nome_serv:
                st.session_state.itens_recibo.append({"servico": nome_serv, "valor": valor_serv})
                st.rerun()

    with col2:
        st.markdown("### Resumo do Recibo")
        total_recibo = sum(item["valor"] for item in st.session_state.itens_recibo)
        
        if len(st.session_state.itens_recibo) > 0:
            for item in st.session_state.itens_recibo:
                st.write(f"- {item['servico']}: **R$ {formatar_moeda(item['valor'])}**")
            st.markdown(f"**Total: R$ {formatar_moeda(total_recibo)}**")
            if st.button("Limpar Lista"):
                st.session_state.itens_recibo = []
                st.rerun()
        else:
            st.warning("Nenhum serviço adicionado.")

    st.divider()

    if st.button("Gerar Recibo em PDF e Salvar", type="primary", use_container_width=True):
        if nome_pagador.strip() and len(st.session_state.itens_recibo) > 0:
            for item in st.session_state.itens_recibo:
                catalogo[item["servico"]] = item["valor"]
            salvar_json(catalogo, ARQUIVO_CATALOGO)
            
            historico.append({
                "data": data_recibo.strftime("%Y-%m-%d"),
                "cliente": nome_pagador,
                "servicos": [i["servico"] for i in st.session_state.itens_recibo],
                "total": total_recibo
            })
            salvar_json(historico, ARQUIVO_HISTORICO)

            buffer_rec = BytesIO()
            pdf_rec = canvas.Canvas(buffer_rec, pagesize=A4)
            largura, altura = A4

            desenhar_cabecalho_rodape(pdf_rec, "RECIBO")
            
            pdf_rec.setFillColor(COR_TEXTO)
            pdf_rec.setFont("Helvetica", 10)
            pdf_rec.drawString(largura - 150, altura - 130, f"Data: {data_recibo.strftime('%d/%m/%Y')}")

            str_total = formatar_moeda(total_recibo)

            pdf_rec.setFillColor(COR_CINZA)
            pdf_rec.setStrokeColor(COR_AZUL_CLARO)
            pdf_rec.setLineWidth(1.5)
            pdf_rec.roundRect(largura - 200, altura - 200, 150, 40, 5, fill=True, stroke=True)
            pdf_rec.setFillColor(COR_AZUL_ESCURO)
            pdf_rec.setFont("Helvetica-Bold", 16)
            pdf_rec.drawCentredString(largura - 125, altura - 188, f"R$ {str_total}")

            if len(st.session_state.itens_recibo) > 1:
                texto_base = f"Recebemos de {nome_pagador}, o valor de R$ {str_total} referente aos serviços descritos abaixo:"
            else:
                texto_base = f"Recebemos de {nome_pagador}, o valor de R$ {str_total} referente ao serviço descrito abaixo:"
            
            desenhar_texto_com_quebra(pdf_rec, texto_base, 60, altura - 230, max_width=largura - 120, fonte="Helvetica", tamanho=12)

            y_tabela = altura - 280
            pdf_rec.setFillColor(COR_AZUL_ESCURO)
            pdf_rec.setFont("Helvetica-Bold", 12)
            pdf_rec.drawString(60, y_tabela, "Serviços Prestados" if len(st.session_state.itens_recibo) > 1 else "Serviço Prestado")
            pdf_rec.drawString(largura - 150, y_tabela, "Valor")
            pdf_rec.line(60, y_tabela - 5, largura - 60, y_tabela - 5)
            
            y_tabela -= 25
            pdf_rec.setFillColor(COR_TEXTO)
            pdf_rec.setFont("Helvetica", 11)
            for item in st.session_state.itens_recibo:
                str_item = formatar_moeda(item['valor'])
                
                pdf_rec.drawString(60, y_tabela, f"• {item['servico']}")
                pdf_rec.drawString(largura - 150, y_tabela, f"R$ {str_item}")
                pdf_rec.setStrokeColor(COR_CINZA)
                pdf_rec.setLineWidth(0.5)
                pdf_rec.line(60, y_tabela - 5, largura - 60, y_tabela - 5)
                y_tabela -= 20

            y_final = y_tabela - 30
            pdf_rec.setFont("Helvetica", 10)
            pdf_rec.drawString(60, y_final, "Para maior clareza, firmamos o presente recibo para que produza os seus efeitos legais.")

            meses = ["", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
            local_data = f"Brazlândia - DF, {data_recibo.day} de {meses[data_recibo.month]} de {data_recibo.year}."
            pdf_rec.setFont("Helvetica-Oblique", 12)
            pdf_rec.drawCentredString(largura / 2, y_final - 40, local_data)

            pdf_rec.setStrokeColor(COR_AZUL_ESCURO)
            pdf_rec.line(largura/2 - 120, y_final - 110, largura/2 + 120, y_final - 110)
            pdf_rec.setFillColor(COR_AZUL_ESCURO)
            pdf_rec.setFont("Helvetica-Bold", 12)
            pdf_rec.drawCentredString(largura / 2, y_final - 125, "EDSON PORTÕES")

            pdf_rec.save()
            buffer_rec.seek(0)
            st.success("Recibo gerado e histórico atualizado!")
            st.download_button("Baixar Recibo PDF", buffer_rec, f"Recibo_{nome_pagador}.pdf")
        else:
            st.warning("Preencha o Nome e adicione pelo menos um serviço.")