# Automação de Lançamento de Despesas — Sistema Interno ERP Web

Script em Python + Selenium para automatizar o lançamento de despesas em um sistema 
interno ERP Web, eliminando o trabalho manual e repetitivo de preencher formulários 
um por um.

## Como funciona
1. Conecta a uma sessão do Chrome já aberta e logada (via porta de depuração remota)
2. Busca o evento (PP) pelo número
3. Preenche automaticamente Centro de Custo, Destinatário, Forma de Pagamento, 
   Vencimento, Data NF e Valor
4. Confirma o lançamento e repete o processo para múltiplas despesas/PPs

## Requisitos
- Python 3.x
- Selenium (`pip install selenium`)
- Google Chrome aberto com depuração remota na porta 9222

---

## Histórico de Versões

### v1.1 — Espera inteligente na busca de eventos
**Problema:** o script usava um tempo fixo de espera (`time.sleep`) antes de tentar 
clicar no resultado da busca por PP. Em momentos de internet ou computador mais lentos, 
esse tempo podia não ser suficiente, causando o erro `IndexError: list index out of range` 
(a lista de resultados ainda estava vazia quando o script tentava acessá-la).

**Solução:** substituído o tempo fixo por uma condição de espera ativa 
(`wait.until`), que verifica repetidamente se já existe pelo menos 1 resultado 
na tela antes de prosseguir — aguardando o tempo necessário, seja ele maior ou menor.

**Bônus:** se a PP não for encontrada após o tempo máximo de espera, o script agora 
lança um erro claro (`"PP {numero} não encontrada — confira se o número está correto"`) 
em vez de um erro genérico e confuso.

### v1.0 — Versão inicial
- Fluxo completo de busca de evento, inclusão de despesa e confirmação
- Suporte a múltiplos lançamentos em múltiplas PPs no mesmo script
- Aviso visual (popup do Windows) ao final da execução