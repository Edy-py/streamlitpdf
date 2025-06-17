# streamlitpdf

Este projeto tem como objetivo principal explorar a geração de PDFs utilizando a biblioteca ReportLab em conjunto com o Streamlit, e posteriormente, realizar o deploy da aplicação na nuvem utilizando o Streamlit Community Cloud.

## Sobre o Autor

**Edilson Alves da Silva**
Graduando do 3º período de Ciência da Computação na Universidade Federal de Catalão (UFCAT).

## Funcionalidades

A aplicação permite a criação de orçamentos em PDF de forma interativa. O usuário pode inserir as seguintes informações:

* Nome do cliente
* Email do cliente
* Descrição do serviço (com quebra de linha automática para textos longos)
* Valor total do serviço
* Forma de pagamento (Pix/Dinheiro, Débito, Crédito à vista, Crédito parcelado)
* Quantidade de parcelas (se a forma de pagamento for "Crédito parcelado")

Após preencher os dados, um botão "Gerar Pdf" permite baixar o orçamento em formato PDF.

## Tecnologias Utilizadas

* Python
* Streamlit
* ReportLab

## Como Executar o Projeto Localmente

1.  **Clone o repositório:**

    ```bash
    git clone [https://github.com/seu-usuario/streamlitpdf.git](https://github.com/seu-usuario/streamlitpdf.git)
    ```

2.  **Navegue até o diretório do projeto:**

    ```bash
    cd streamlitpdf
    ```

3.  **Crie e ative um ambiente virtual (opcional, mas recomendado):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

4.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Execute a aplicação Streamlit:**

    ```bash
    streamlit run app_gera_pdf.py
    ```

    A aplicação será aberta automaticamente no seu navegador padrão.

## Deploy no Streamlit Community Cloud

O objetivo final deste projeto é realizar o deploy no Streamlit Community Cloud, tornando a aplicação acessível publicamente.

## Estrutura do Projeto

* `app_gera_pdf.py`: Contém o código principal da aplicação Streamlit, responsável pela interface do usuário e geração do PDF.
* `requirements.txt`: Lista todas as bibliotecas Python necessárias para o projeto.
* `.gitignore`: Define os arquivos e diretórios a serem ignorados pelo Git (ex: `venv/`).
* `README.md`: Este arquivo, descrevendo o projeto.
