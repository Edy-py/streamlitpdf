import streamlit as st
import aba_orcamento
import aba_recibo
import aba_dash

from pdf_utils import LOGO

st.set_page_config(page_title="Edson Portões - Sistema", page_icon=LOGO, layout="wide")

# Inicializa sessão para os carrinhos de serviços
if 'itens_recibo' not in st.session_state:
    st.session_state.itens_recibo = []
if 'itens_orcamento' not in st.session_state:
    st.session_state.itens_orcamento = []

st.title("Edson Portões - Sistema de Gestão")

tab1, tab2, tab3 = st.tabs(["📄 Gerar Orçamento", "🧾 Gerar Recibo", "📊 Dashboard"])

with tab1:
    aba_orcamento.renderizar()

with tab2:
    aba_recibo.renderizar()

with tab3:
    aba_dash.renderizar()