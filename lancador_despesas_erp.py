"""
Lançador de Despesas - Automação com Selenium

Este script automatiza o lançamento de despesas em eventos cadastrados
em um sistema de gestão interno (ERP web), evitando a necessidade de
preencher manualmente o mesmo formulário repetidas vezes.

Como funciona:
    1. Conecta a uma sessão do Chrome já aberta e logada manualmente
    2. Busca o evento pelo número informado
    3. Abre o formulário de nova despesa
    4. Preenche automaticamente centro de custo, destinatário, forma de
       pagamento, datas e valor
    5. Confirma o lançamento e repete para os próximos itens da lista

Pré-requisitos:
    - Ter o Chrome aberto em modo de depuração remota (porta 9222)
    - Estar logado manualmente no sistema antes de rodar o script
    - Biblioteca: selenium
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import tkinter as tk
from tkinter import messagebox

def mostrar_aviso(mensagem):
    janela = tk.Tk()
    janela.attributes('-topmost', True)   # força ficar na frente de tudo
    janela.withdraw()                      # esconde a janela principal (só queremos o popup)
    messagebox.showinfo("Aviso", mensagem, parent=janela)
    janela.destroy()                       # fecha a janela escondida depois do OK


# Conecta no Chrome que já está aberto (porta 9222)
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)


def buscar_evento(numero_pp):
    campo_numero = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[id$='numero']")))
    campo_numero.clear()
    campo_numero.send_keys(str(numero_pp))

    botao_pesquisar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id$='bt_2']")))
    botao_pesquisar.click()

    # Aqui mantemos uma pequena espera fixa: o risco não é "elemento não existir ainda",
    # é existir mais de um (o novo + fantasmas de buscas antigas), então o tempo garante
    # que o resultado novo já foi desenhado antes de contarmos quantos existem.
    time.sleep(1.5)

    candidatos = driver.find_elements(By.CSS_SELECTOR, "[id$='_2_0']")
    elemento_texto = candidatos[-1]
    elemento_linha = elemento_texto.find_element(By.XPATH, "..")
    elemento_linha.click()


def clicar_incluir():
    botao_incluir = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id$='bt3']")))
    botao_incluir.click()


def clicar_despesa():
    botao_despesa = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id$='bt2']")))
    botao_despesa.click()


def preencher_despesa(centro_custo_valor, destinatario_valor, forma_valor, vencimento, data_nf, valor):
    select_centro_el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[id$='id_custo']")))
    Select(select_centro_el).select_by_value(str(centro_custo_valor))

    select_destinatario_el = driver.find_element(By.CSS_SELECTOR, "[id$='id_fornecedor']")
    Select(select_destinatario_el).select_by_value(str(destinatario_valor))

    select_forma_el = driver.find_element(By.CSS_SELECTOR, "[id$='id_forma']")
    Select(select_forma_el).select_by_value(str(forma_valor))

    campo_vencimento = driver.find_element(By.CSS_SELECTOR, "[id$='vencimento']")
    campo_vencimento.clear()
    campo_vencimento.send_keys(vencimento)

    campo_data_nf = driver.find_element(By.CSS_SELECTOR, "[id$='data_nf']")
    campo_data_nf.clear()
    campo_data_nf.send_keys(data_nf)

    campo_valor = driver.find_element(By.CSS_SELECTOR, "[id$='valor']")
    campo_valor.click()
    campo_valor.send_keys(Keys.CONTROL, 'a')
    campo_valor.send_keys(Keys.DELETE)
    campo_valor.send_keys(str(valor))


def clicar_incluir_despesa():
    botao_incluir = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id$='bt3']")))
    botao_incluir.click()


def clicar_ok():
    botao_ok = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id$='bt_ok']")))
    botao_ok.click()


def voltar_para_eventos():
    menu_eventos = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id$='menu_7']")))
    menu_eventos.click()


def lancar_despesa(centro_custo_valor, destinatario_valor, forma_valor, vencimento, data_nf, valor):
    """Faz um lançamento completo: Incluir > Despesa > preencher > Incluir > Ok"""
    clicar_incluir()
    clicar_despesa()
    preencher_despesa(
        centro_custo_valor=centro_custo_valor,
        destinatario_valor=destinatario_valor,
        forma_valor=forma_valor,
        vencimento=vencimento,
        data_nf=data_nf,
        valor=valor
    )
    clicar_incluir_despesa()
    clicar_ok()


# ===================================================
# EXECUÇÃO — cole aqui embaixo os seus lançamentos
# ===================================================

# ---------- Exemplo de evento 1 ----------
buscar_evento(436)

lancar_despesa(centro_custo_valor=83, destinatario_valor=1012, forma_valor=51,
                vencimento="09/09/2026", data_nf="31/07/2026", valor="50.00")

lancar_despesa(centro_custo_valor=18, destinatario_valor=1011, forma_valor=51,
                vencimento="09/09/2026", data_nf="04/08/2026", valor="193.00")

voltar_para_eventos()

# ---------- Exemplo de evento 2 ----------
buscar_evento(190)

lancar_despesa(centro_custo_valor=83, destinatario_valor=1012, forma_valor=51,
                vencimento="09/09/2026", data_nf="31/07/2026", valor="120.00")

voltar_para_eventos()

time.sleep(1)

mostrar_aviso("Todos os lançamentos foram concluídos!")
