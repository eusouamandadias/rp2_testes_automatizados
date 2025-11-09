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

# login
def login(driver):
    driver.get(URL)
    time.sleep(5)
    json_str = json.dumps(FBASE_VALUE)
    # Usa backticks no JS para preservar qualquer caractere no JSON
    script = f"window.localStorage.setItem({json.dumps(FBASE_KEY)}, `{json_str}`);"
    driver.execute_script(script)
    driver.execute_script("window.location.reload();")
    time.sleep(5)
    print("Login efetuado e página recarregada.")

# Executar caso de teste 17
def testar_consulta_de_alunos(driver):
    wait = WebDriverWait(driver, 5)

    # Clicar na foto de perfil no topo da página.
    print("Clicando no avatar de perfil")
    imagem_perfil = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.MuiAvatar-img")))
    driver.execute_script("arguments[0].click();", imagem_perfil)  # fallback caso o click normal falhe
    time.sleep(5)

    # Selecionar opção “Gerenciamento de Cursos”
    print("Gerenciamento de Cursos...")
    gerenciamento = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Gerenciamento de Cursos')]"))
    )
    driver.execute_script("arguments[0].click();", gerenciamento)
    time.sleep(5)

    # Clicar na opção “Gerenciar Curso”, no curso desejado
    print("Selecionando curso")
    gerenciar_botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Gerenciar Curso')]")))
    gerenciar_botao.click()
    time.sleep(5)

    # Selecionar a opção “Alunos”
    print("Abrindo aba de alunos")
    alunos_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alunos')]")))
    alunos_tab.click()
    time.sleep(5)

    # Verificar se a lista de alunos é exibida
    print("Verificando lista de alunos")
    alunos_linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    if len(alunos_linhas) > 0:
        print(f"Lista encontrada! Total de alunos listados: {len(alunos_linhas)}")
        # Pegando dados da primeira linha como exemplo
        primeira_linha = alunos_linhas[0].text
        print("Registro: ", primeira_linha)
    else:
        print("Nenhum aluno encontrado na lista!")

# MAIN
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login(driver)
        testar_consulta_de_alunos(driver)
    finally:
        time.sleep(5)
        driver.quit()
        print("Teste finalizado")
