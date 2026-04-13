# Diretriz: Geração de PDF de Orçamento

Esta diretriz descreve o processo de geração de orçamento em PDF.

## Entradas

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `nome` | string | Sim | Nome do cliente |
| `email` | string | Sim | Email do cliente |
| `descricao` | string | Sim | Detalhes do serviço |
| `valor` | string | Sim | Valor total do serviço |
| `forma_pagamento` | string | Sim | Ex: Pix, Débito, Crédito |
| `parcelas` | string | Não | Quantidade de parcelas (se aplicável) |

## Processamento

1. **Validação**: Verifica se os campos obrigatórios estão preenchidos (atualmente feito no frontend).
2. **Criação do Canvas**: Utiliza `reportlab.pdfgen.canvas` em um buffer de memória (`io.BytesIO`).
3. **Cabeçalho**: Insere dados da empresa (Edson Portões, CNPJ, Telefone).
4. **Dados do Cliente**: Insere nome, email, valor e forma de pagamento.
5. **Descrição**: Quebra o texto da descrição em linhas para caber na largura da página (wrap).
6. **Finalização**: Salva o PDF no buffer.

## Saída

- Objeto `io.BytesIO` contendo o arquivo PDF binário, pronto para download.

## Edge Cases

- **Descrição Longa**: O texto é quebrado automaticamente, mas não há paginação implementada. Textos muito longos podem extrapolar a página única.
- **Caracteres Especiais**: O encoding padrão do ReportLab deve lidar com UTF-8, mas caracteres não suportados pela fonte podem falhar.
