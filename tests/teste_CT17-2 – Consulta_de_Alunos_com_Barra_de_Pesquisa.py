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

# Executar Caso de Teste 17-2
def testar_consulta_de_alunos_com_barra_de_pesquisa(drive):
    wait = WebDriverWait(driver, 15)

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
    curso_card = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'MuiCard-root')][.//h6[normalize-space(text())='Teste Avaliação']]")
    ))

    gerenciar_btn = curso_card.find_element(By.XPATH, ".//button[contains(., 'Gerenciar Curso')]")
    driver.execute_script("arguments[0].click();", gerenciar_btn)
    time.sleep(2)

    # Abrir aba "Alunos"
    print("Abrindo aba de alunos...")
    alunos_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alunos')]")))
    alunos_tab.click()
    time.sleep(2)

    # Digitar na barra de pesquisa
    campo_pesquisa = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Buscar estudante por nome ou email...']")
    ))
    campo_pesquisa.clear()
    campo_pesquisa.send_keys("Sidnei")
    time.sleep(5)

    # Validar resultado da tabela após filtro
    print("Validando resultado do filtro...")
    linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    if len(linhas) == 0:
        print("Nenhum aluno encontrado após a pesquisa.")
    else:
        print(f"{len(linhas)} aluno(s) encontrado(s):")
        for linha in linhas:
            texto = linha.text.lower()
            if "Sidnei" in texto:
                print("   → OK:", linha.text)

# MAIN
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        testar_consulta_de_alunos_com_barra_de_pesquisa(driver)
    finally:
        time.sleep(6)
        driver.quit()
        print("Teste finalizado")
