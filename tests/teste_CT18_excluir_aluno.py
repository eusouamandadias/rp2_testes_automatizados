import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://testes.codefolio.com.br/"

# Configuração Selenium
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Sessão Firebase
def login_firebase(driver):
    driver.get(URL)
    time.sleep(1)
    json_str = json.dumps(FBASE_VALUE)
    # Usa backticks no JS para preservar qualquer caractere no JSON
    script = f"window.localStorage.setItem({json.dumps(FBASE_KEY)}, `{json_str}`);"
    driver.execute_script(script)
    driver.execute_script("window.location.reload();")
    time.sleep(4)
    print("Login efetuado e página recarregada.")

# Executar Caso de Teste 18-1
def testar_consulta_de_alunos_se_o_Aluno_Ainda_Aparece_na_Lista_Apos_sua_Remoção(driver):
    wait = WebDriverWait(driver, 5)

    # Clicar na foto de perfil
    print("Clicando no avatar de perfil")
    imagem_perfil = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.MuiAvatar-img")))
    driver.execute_script("arguments[0].click();", imagem_perfil)
    time.sleep(1)

    # Selecionar “Gerenciamento de Cursos”
    print("Abrindo Gerenciamento de Cursos...")
    gerenciamento = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Gerenciamento de Cursos')]"))
    )
    driver.execute_script("arguments[0].click();", gerenciamento)
    time.sleep(1)

    # Selecionar o curso
    print("Selecionando curso 'Teste Avaliação'")
    curso = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'MuiCard-root')][.//h6[normalize-space(text())='Teste Avaliação']]")
    ))

    botao_gerenciar = curso.find_element(By.XPATH, ".//button[contains(., 'Gerenciar Curso')]")
    driver.execute_script("arguments[0].click();", botao_gerenciar)
    time.sleep(2)

    # Abrir aba "Alunos"
    print("Abrindo aba de alunos...")
    alunos = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alunos')]")))
    alunos.click()
    time.sleep(6)

    # Selecionar primeira linha (primeiro aluno da lista)
    primeira_linha = wait.until(EC.presence_of_element_located(
        (By.XPATH, "(//table//tr)[2]") # TR[1] é cabeçalho
    ))

    # Captura o nome do aluno que será removido (para validação)
    aluno_nome = primeira_linha.find_element(By.XPATH, ".//td[1]").text
    print(f"Aluno a ser excluído: {aluno_nome}")

    # Botão de excluir dentro dessa linha
    botao_excluir = primeira_linha.find_element(By.XPATH, ".//button[.//*[@data-testid='DeleteIcon']]")
    driver.execute_script("arguments[0].click();", botao_excluir)
    time.sleep(8)

    # Clicar no botão Confirmar
    confirm_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Confirmar')]"))
    )
    driver.execute_script("arguments[0].click();", confirm_btn)

    # Esperar mensagem de confirmação
    try:
        mensagem_sucesso = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".MuiSnackbar-root, .MuiAlert-root")
            )
        )
        print("Mensagem:", mensagem_sucesso.text)
    except:
        print("Não apareceu mensagem de sucesso.")
        

    # Verificar se aluno sumiu da lista
    recaregar_pagina = driver.page_source

    if aluno_nome not in recaregar_pagina:
        print("O aluno foi removido corretamente da lista.")
    else:
        print("O aluno ainda aparece na lista após remoção.")

# MAIN
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        testar_consulta_de_alunos_se_o_Aluno_Ainda_Aparece_na_Lista_Apos_sua_Remoção(driver)
    finally:
        time.sleep(5)
        driver.quit()
        print("Teste finalizado")