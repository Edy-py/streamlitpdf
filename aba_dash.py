import streamlit as st
import pandas as pd
from db import carregar_json, ARQUIVO_HISTORICO
from pdf_utils import formatar_moeda

def renderizar():
    st.header("Visão Geral do Negócio")
    
    historico = carregar_json(ARQUIVO_HISTORICO)
    
    if len(historico) > 0:
        df = pd.DataFrame(historico)
        df['data'] = pd.to_datetime(df['data'])
        df['mes_ano'] = df['data'].dt.to_period('M').astype(str)
        
        total_geral = df['total'].sum()
        
        df_clientes = df.groupby('cliente').agg(
            total_gasto=('total', 'sum'),
            frequencia=('cliente', 'count')
        ).reset_index()
        
        cliente_ouro = df_clientes.sort_values('total_gasto', ascending=False).iloc[0]
        cliente_frequente = df_clientes.sort_values('frequencia', ascending=False).iloc[0]
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento Total", f"R$ {formatar_moeda(total_geral)}")
        c2.metric("Cliente Ouro", f"{cliente_ouro['cliente']}", f"R$ {formatar_moeda(cliente_ouro['total_gasto'])}")
        c3.metric("Cliente Mais Frequente", f"{cliente_frequente['cliente']}", f"{cliente_frequente['frequencia']} serviços")
        
        st.divider()
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar Histórico (CSV)",
            data=csv,
            file_name="historico_edson_portoes.csv",
            mime="text/csv",
            type="primary"
        )
        
        col_grafico, col_tabela = st.columns([1, 1])
        with col_grafico:
            st.markdown("### Faturamento por Mês")
            faturamento_mensal = df.groupby('mes_ano')['total'].sum().reset_index()
            st.bar_chart(data=faturamento_mensal, x='mes_ano', y='total', color="#008FD3")
            
        with col_tabela:
            st.markdown("### Últimos Serviços Realizados")
            df_exibicao = df[['data', 'cliente', 'servicos', 'total']].sort_values('data', ascending=False).head(10)
            df_exibicao['data'] = df_exibicao['data'].dt.strftime('%d/%m/%Y')
            df_exibicao['servicos'] = df_exibicao['servicos'].apply(lambda x: ", ".join(x))
            st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
            
    else:
        st.info("Nenhum dado registrado ainda. Gere recibos para popular o Dashboard.")