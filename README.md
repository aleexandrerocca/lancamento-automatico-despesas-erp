# Lançador de Despesas

Automação em Python que preenche e lança despesas automaticamente em eventos cadastrados em um sistema de gestão interno (ERP web), eliminando a necessidade de digitar os mesmos dados repetidamente em um formulário manual.

> **Nota:** este é um projeto amador, feito por mim enquanto estou aprendendo Python e automação. Não é um sistema profissional nem revisado por especialistas — é um projeto de estudo, construído pra resolver um problema real do meu dia a dia de trabalho. Fico aberto a sugestões e feedbacks!

## 💡 O problema que esse projeto resolve

Lançar despesas de eventos no sistema exige repetir o mesmo processo manual várias vezes: abrir o formulário, escolher o centro de custo, o destinatário, a forma de pagamento, digitar datas e valores — um por um. Quando há vários lançamentos parecidos para vários eventos, isso consome bastante tempo e aumenta o risco de erro de digitação.

Esse script automatiza esse processo: você define os lançamentos que quer fazer (evento, centro de custo, valor, datas, etc.), e ele preenche e confirma tudo sozinho, exatamente como se fosse feito manualmente.

## 📊 Impacto

Antes da automação, lançar as despesas de um lote de eventos levava, em média, entre
**4 e 6 horas** de trabalho manual e repetitivo. Com o script, esse mesmo processo passou
a levar cerca de **15 a 20 minutos** — considerando o tempo de coletar os dados das notas
e rodar o script (que executa os lançamentos sozinho, sem necessidade de acompanhamento
constante).

> Esses números são uma estimativa pessoal baseada na minha rotina de trabalho, não um
> benchmark formal — mas dão uma boa noção do ganho real de tempo que a automação trouxe.

## ⚙️ Como funciona

1. **Conecta a uma sessão do Chrome já aberta**, com login já feito manualmente (por segurança, o script nunca lida com senhas)
2. **Busca o evento** pelo número informado
3. **Abre o formulário de nova despesa** (clica em "Incluir" → "Despesa")
4. **Preenche automaticamente** os campos: centro de custo, destinatário, forma de pagamento, data de vencimento, data da nota fiscal e valor
5. **Confirma o lançamento** e repete o processo para cada item da lista
6. Ao final, mostra um **aviso na tela** confirmando que todos os lançamentos foram concluídos

## 🛠️ Tecnologias usadas

- **Python**
- **Selenium** — automação do navegador
- **Tkinter** — exibição do aviso final na tela

## 🚀 Como rodar

### Pré-requisitos

- Python 3.10 ou superior instalado
- Google Chrome instalado

### 1. Instale as dependências

```bash
pip install selenium
```

(o Tkinter já vem instalado por padrão com o Python na maioria dos sistemas)

### 2. Abra o Chrome em modo de depuração remota

O script se conecta a uma janela do Chrome que você já abriu e já logou manualmente no sistema (assim, credenciais nunca passam pelo código). Para abrir o Chrome nesse modo, rode no terminal:

**Windows:**
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

**Mac/Linux:**
```bash
google-chrome --remote-debugging-port=9222
```

### 3. Faça login manualmente

Com essa janela do Chrome aberta, acesse o sistema e faça login normalmente, como você faria de costume.

### 4. Edite a lista de lançamentos

Abra o arquivo `lancador_despesas_erp.py` e edite a seção de execução, no final do arquivo, com os eventos e valores que você quer lançar:

```python
buscar_evento(436)

lancar_despesa(centro_custo_valor=83, destinatario_valor=1012, forma_valor=51,
                vencimento="09/09/2026", data_nf="31/07/2026", valor="50.00")

voltar_para_eventos()
```

### 5. Rode o script

```bash
python lancador_despesas_erp.py
```

Ao final, uma janela de aviso confirma que todos os lançamentos foram feitos.

## 📁 O que cada arquivo faz

| Arquivo | O que faz |
|---|---|
| `lancador_despesas_erp.py` | Script principal — roda os lançamentos automaticamente |

## ⚠️ Aviso

Este projeto foi feito para uso com um sistema interno específico de uma empresa. Os seletores CSS usados no código (nomes de campos, botões, etc.) são específicos daquele sistema e provavelmente não vão funcionar em outro ERP sem ajustes. O código está aqui como exemplo de solução para um problema real de automação web.

## 📌 Possíveis melhorias futuras

- [ ] Fazer o script anexar automaticamente uma imagem (nota fiscal/comprovante) no sistema, logo após lançar o valor
- [ ] Usar OCR (reconhecimento de texto em imagens) para ler automaticamente a data, o valor e a descrição direto de uma foto da nota fiscal, preenchendo o formulário sem precisar digitar essas informações manualmente
- [ ] Combinar OCR + automação para um fluxo completo: tirar foto do comprovante → extrair os dados → lançar automaticamente, do início ao fim
- [ ] Ler a lista de lançamentos a partir de um arquivo externo (Excel/CSV), em vez de editar o código a cada uso
- [ ] Adicionar tratamento de erros por lançamento, para que um erro em um item não interrompa os demais