import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuração Selenium
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Sessão Firebase
def login_firebase(driver):
    driver.get(URL)
    time.sleep(3)
    json_str = json.dumps(FBASE_VALUE)
    # Usa backticks no JS para preservar qualquer caractere no JSON
    script = f"window.localStorage.setItem({json.dumps(FBASE_KEY)}, `{json_str}`);"
    driver.execute_script(script)
    driver.execute_script("window.location.reload();")
    time.sleep(3)
    print("Login efetuado e página recarregada.")

# Executar Caso de Teste 17-1
def testar_consulta_de_alunos_sem_alunos(driver):
    wait = WebDriverWait(driver, 3)

    # Clicar na foto de perfil no topo da página.
    print("Clicando no avatar de perfil")
    imagem_perfil = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.MuiAvatar-img")))
    driver.execute_script("arguments[0].click();", imagem_perfil)  # fallback caso o click normal falhe
    time.sleep(3)


    # Selecionar opção “Gerenciamento de Cursos”
    print("Gerenciamento de Cursos...")
    gerenciamento = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Gerenciamento de Cursos')]"))
    )
    driver.execute_script("arguments[0].click();", gerenciamento)
    time.sleep(3)

    # Encontra o card cujo título <h6> seja exatamente "Testess"
    curso_card = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'MuiCard-root')][.//h6[normalize-space(text())='Testess']]")
    ))

    # Dentro desse card, pega o botão Gerenciar Curso
    gerenciar_btn = curso_card.find_element(By.XPATH, ".//button[contains(., 'Gerenciar Curso')]")

    driver.execute_script("arguments[0].click();", gerenciar_btn)
    time.sleep(3)

    # Selecionar a opção “Alunos”
    print("Abrindo aba de alunos")
    alunos_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alunos')]")))
    alunos_tab.click()
    time.sleep(5)

    # Verificar se a lista de alunos é exibida
    print("Verificando lista de alunos")
    alunos_linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    if len(alunos_linhas) == 0:
        print("Nenhum aluno encontrado na lista!")

# MAIN
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        testar_consulta_de_alunos_sem_alunos(driver)
    finally:
        time.sleep(8)
        driver.quit()
        print("Teste finalizado")
