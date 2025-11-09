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
def testar_cancelar_exclusao_aluno(driver):
    wait = WebDriverWait(driver, 15)

    # Clicar na foto de perfil
    imagem_perfil = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.MuiAvatar-img")))
    driver.execute_script("arguments[0].click();", imagem_perfil)

    # Selecionar “Gerenciamento de Cursos”
    gerenciamento = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Gerenciamento de Cursos')]")))
    driver.execute_script("arguments[0].click();", gerenciamento)

    # Selecionar curso
    curso = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'MuiCard-root')][.//h6[normalize-space(text())='Teste Avaliação']]")
    ))
    botao_gerenciar = curso.find_element(By.XPATH, ".//button[contains(., 'Gerenciar Curso')]")
    driver.execute_script("arguments[0].click();", botao_gerenciar)

    # Abrir aba Alunos
    alunos_aba = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alunos')]")))
    alunos_aba.click()

    # Capturar primeiro aluno da lista
    primeira_linha = wait.until(EC.presence_of_element_located((By.XPATH, "(//table//tr)[2]")))
    aluno_nome = primeira_linha.find_element(By.XPATH, ".//td[1]").text
    print(f"Aluno selecionado para exclusão (que será cancelada): {aluno_nome}")

    # Clicar em excluir
    botao_excluir = primeira_linha.find_element(By.XPATH, ".//button[.//*[@data-testid='DeleteIcon']]")
    driver.execute_script("arguments[0].click();", botao_excluir)

    # Esperar modal e clicar em Cancelar
    modal = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@role,'dialog')]"))
    )
    botao_cancelar = modal.find_element(
        By.XPATH, ".//button[contains(., 'Cancelar')]"
    )
    driver.execute_script("arguments[0].click();", botao_cancelar)
    
    print("Clique em 'Cancelar' realizado.")

    # Verificar se aluno ainda aparece na lista
    alunos_lista = driver.find_elements(By.XPATH, "//table//tr/td[1]")
    nomes = [a.text for a in alunos_lista]

    if aluno_nome in nomes:
        print("O aluno foi removido mesmo após cancelar a exclusão.")
    else:
        print("O aluno ainda aparece na lista após cancelar a exclusão.")


# MAIN
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        testar_cancelar_exclusao_aluno(driver)
    finally:
        time.sleep(2)
        driver.quit()
        print("Teste finalizado")