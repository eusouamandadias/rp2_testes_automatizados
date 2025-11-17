import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys


URL = "https://testes.codefolio.com.br/"

# === Dados de login Firebase ===
FBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
FBASE_VALUE = {
  "apiKey": "AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg",
  "appName": "[DEFAULT]",
  "createdAt": "1760400630739",
  "displayName": "Mariana Ferrao Chuquel",
  "email": "marianachuquel.aluno@unipampa.edu.br",
  "emailVerified": True,
  "isAnonymous": False,
  "lastLoginAt": "1762094148472",
  "phoneNumber": None,
  "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocJDeohS-IjOHZEhkc1yPLhPjjR_NtR-5eg6pCH4RtYjb8k8Gg=s96-c",
  "providerData": [
    {
      "displayName": "Mariana Ferrao Chuquel",
      "email": "marianachuquel.aluno@unipampa.edu.br",
      "phoneNumber": None,
      "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocKT9ZhUhDVhrkG7Sey73w4IyRNo5IOZS4rXRAeWGYAEB3bUCl3P=s96-c",
      "providerId": "google.com",
      "uid": "104954081519398196990"
    }
  ],
  "stsTokenManager": {
    "accessToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NTEzMjA5OWFkNmJmNjEzODJiNmI0Y2RlOWEyZGZlZDhjYjMwZjAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTWFyaWFuYSBGZXJyYW8gQ2h1cXVlbCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NKRGVvaFMtSWpPSFpFaGtjMXlQTGhQampSX050Ui01ZWc2cENINFJ0WWpiOGs4R2c9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vcmVhY3QtbmEtcHJhdGljYSIsImF1ZCI6InJlYWN0LW5hLXByYXRpY2EiLCJhdXRoX3RpbWUiOjE3NjIwODUxMjEsInVzZXJfaWQiOiJCb2todGdKREREZGxIdG9ad052SEpJT245NHMyIiwic3ViIjoiQm9raHRnSkRERGRsSHRvWndOdkhKSU9uOTRzMiIsImlhdCI6MTc2MjY2MjUxMSwiZXhwIjoxNzYyNjY2MTExLCJlbWFpbCI6Im1hcmlhbmFjaHVxdWVsLmFsdW5vQHVuaXBhbXBhLmVkdS5iciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTA0OTU0MDgxNTE5Mzk4MTk2OTkwIl0sImVtYWlsIjpbIm1hcmlhbmFjaHVxdWVsLmFsdW5vQHVuaXBhbXBhLmVkdS5iciJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.giyO3saQ-WPfhXxUc_j56w1042UjKCwQYcA3MhBWkn6wtN3KncuwXs-oL238A33a5ZqUs74Dl0RFT__n2zR7OhdtE2Bwuf_DH7hd0YYDGqX1LltHd6HYdrLF81OohpvvuyYwtnAEIBSgQ7S7ktYZLC0T95PVuu61ea2viem8J_uLvDWFA5J3UBFfl0KFk5D6k-9GbLAbryI0Yb5Gmw9ly6nH_AvCtBYW-VCO37mmgRmQViDq8dBbNBiKnDIBKF_0b1dLNu7TP7S5tg7qXgz4I0sOQIb5IboNXxE4zWaunYBHNeLf3GBq7S9WwUCS3wgvG1pt4bZ5Ofj72bcCtxFCHQ",
    "expirationTime": 1762666112559,
    "refreshToken": "AMf-vBx6EngbKr8libKojdrdBVe6th750Y3Ma2OJr4gC0tvrVaX5tVgZ0P0V4kBRc3rBWoleGaPQuJFz4aCyha8MtzwzDuMEYXMN8qlNhCQBrN4CJkUHT5IprGHeOCkXQJm44-pyuC2Ssxraklo4b_IjQfcV2HKYqZZ_ZeX6snH187MZh4UiEqGFrsKywP9_NkKLvrUvTiBmJK8msV2etFfxHjwT9w0Wuv0gnhnohgveBtLvm_glWWPwJA3wVGX1zleVr9LBZ0Ar_LR8a9hguunnYUiSUox5N9DBgMmOA6mimHo8QI_rvaGqOLQPOoKi1PMihDskLQL-BtJUikxhPoO1gjCUOpKh1sQIEVf5TbgU3w3P6xPao39gwzgLDUbmMa5VYSkrQCILErXWc27nq6GP6_kHbNp3HTuvLOiDTYxLKiMtOtejG0wR5hl5JnIuODqz1QsjDo2H1qAX45JZ7RWG9q8H8xglpw"
  },
  "tenantId": None,
  "uid": "BokhtgJDDDdlHtoZwNvHJIOn94s2",
  "_redirectEventId": None
}


# === Configuração Selenium ===
def setup_driver():

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

# === Etapa 1: injetar sessão Firebase ===
def login_firebase(driver):
    driver.get(URL)
    time.sleep(1)
    json_str = json.dumps(FBASE_VALUE)
    script = f"window.localStorage.setItem({json.dumps(FBASE_KEY)}, `{json_str}`);"
    driver.execute_script(script)
    driver.execute_script("window.location.reload();")
    time.sleep(4)
    print("✅ Login Firebase injetado e página recarregada.")
    
    
def selecionar_aluno(driver, nome_aluno):
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)

    # Seleciona blocos da lista
    alunos = driver.find_elements(By.CSS_SELECTOR, "div.MuiBox-root.css-1xpn68e")

    for bloco in alunos:
        try:
            # pega o texto do bloco
            texto = bloco.text.upper()

            # Confere se o nome está dentro desse bloco
            if nome_aluno.upper() in texto:
                print(f"👀 Encontrado aluno: {texto}")

                # Scroll até o elemento
                actions.move_to_element(bloco).perform()
                time.sleep(0.3)

                # Clicar no bloco
                bloco.click()
                print(f"✅ Aluno '{nome_aluno}' selecionado!")
                time.sleep(3)
                return True

        except Exception as e:
            print("🛑 Erro ao tentar selecionar aluno:", e)

            
def testar_busca_aluno(driver, nome_busca):
    wait = WebDriverWait(driver, 10)

    # 1) Localiza o campo de busca
    campo_busca = wait.until(
        EC.element_to_be_clickable((
            By.XPATH, "//input[@placeholder='Buscar aluno...']"
        ))
    )

    campo_busca.clear()
    campo_busca.send_keys(nome_busca)
    print("✅ Nome digitado")
    time.sleep(2)  # tempo para MUI atualizar a lista
    
    selecionar_aluno(driver, nome_busca)



         
def realizar_sorteio(driver):
    wait = WebDriverWait(driver, 10)
    print("▶️ Iniciando Passos do CT-27...")

    try:
        # Ir direto para a página de cursos
        driver.get("https://testes.codefolio.com.br/listcurso")
        print("✅ Navegou diretamente para cursos")
        time.sleep(2)

        # 2) Clicar aba Concluídos
        concluidos_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Concluídos')]"))
        )
        driver.execute_script("arguments[0].click();", concluidos_tab)
        print("✅ Clicou na aba Concluídos.")
        time.sleep(1)

        
        cursos = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.MuiCard-root")
        ))

        if len(cursos) < 2:
            print("❌ Não existe um segundo curso na lista!")
            return

        # Seleciona o segundo card
        segundo_curso = cursos[1]
        driver.execute_script("arguments[0].scrollIntoView();", segundo_curso)
        print("✅ Segundo curso encontrado.")

        # 4) Clicar no botão 'Ver Curso' dentro do segundo card
        ver_curso_btn = segundo_curso.find_element(By.XPATH, ".//button[contains(., 'Ver Curso')]")
        driver.execute_script("arguments[0].click();", ver_curso_btn)
        print("✅ Clicou em 'Ver Curso' do segundo curso com sucesso!")
        time.sleep(2)
        
        abrir_quiz = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Abrir Quiz Gigi']"))
        )
        time.sleep(5)
        driver.execute_script("arguments[0].click();", abrir_quiz)
        print("✅ Clicou no botão 'Abrir Quiz Gigi' com sucesso!")
        time.sleep(3)
        
        escolher_aluno = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Escolher outro aluno']"))
        )

        driver.execute_script("arguments[0].click();", escolher_aluno)
        print("✅ Clicou em 'Escolher outro aluno' com sucesso!")
        time.sleep(5)
        
        testar_busca_aluno(driver, "LUIZ")

    except Exception as e:
        print(f"\n🛑 Erro durante a execução do teste: {e}")
        print(f"URL Atual: {driver.current_url}")

        
# === MAIN ===
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        realizar_sorteio(driver)
    finally:
        time.sleep(2)
        driver.quit()
        print("🚪 Teste finalizado e navegador fechado.")
