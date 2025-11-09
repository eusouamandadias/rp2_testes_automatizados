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
def testar_cancelar_exclusao_aluno_sem_alunos_matriculados(driver):
    wait = WebDriverWait(driver, 15)

    # Clicar na foto de perfil no topo da página.
    print("Clicando no avatar de perfil")
    imagem_perfil = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.MuiAvatar-img")))
    driver.execute_script("arguments[0].click();", imagem_perfil)  # fallback caso o click normal falhe
    time.sleep(1)


    # Selecionar opção “Gerenciamento de Cursos”
    print("Gerenciamento de Cursos...")
    gerenciamento = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Gerenciamento de Cursos')]"))
    )
    driver.execute_script("arguments[0].click();", gerenciamento)
    time.sleep(2)

    # Clicar na opção “Gerenciar Curso”, no curso desejado
    print("Selecionando curso 'Teste'")

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
    time.sleep(3)

    # Verificar se aparece a mensagem "Nenhum estudante matriculado neste curso"
    mensagem = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Nenhum estudante matriculado neste curso')]"))
    )

    if mensagem:
        print("Nenhum estudante matriculado neste curso")
    else:
        print("Não apareceu a mensagem")


# MAIN
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        testar_cancelar_exclusao_aluno_sem_alunos_matriculados(driver)
    finally:
        time.sleep(6)
        driver.quit()
        print("Teste finalizado")