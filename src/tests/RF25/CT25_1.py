import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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
    
def teste_sem_atribuir_nota(driver):
    wait = WebDriverWait(driver, 15)
    # Localiza o campo da nota da primeira linha
    campo = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//table//tr[3]//td//input[@type='number']")
    ))

    campo.click()  # ativa o input

    # Clicar fora para tentar salvar
    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(1)

    # Verificar mensagem de erro
    try:
        erro = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'nota inválida') or contains(text(), 'Nota inválida')]")
        ))
        print("✅ Mensagem de erro exibida corretamente:", erro.text)
    except:
        print("❌ ERRO: A mensagem de 'nota inválida' NÃO apareceu.")



def executar_teste_ct25(driver):
    wait = WebDriverWait(driver, 15)
    print("▶️ Iniciando Passos do CT-25 (Acessando Gerenciamento de Cursos)...")
    
    try:
        profile_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']"))
        )

        driver.execute_script("arguments[0].click();", profile_button)
        print("✅ Clicou no botão de perfil (Configurações da Conta) usando JavaScript.")
        time.sleep(1)
        
        
        print("Clicando em 'Gerenciamento de Cursos'...")
        gerenciamento_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[normalize-space()='Gerenciamento de Cursos']"))
        )
        gerenciamento_button.click()
        print("2️⃣ Clicado em 'Gerenciamento de Cursos'.")
        
        print("4️⃣ Clicando no primeiro botão 'Gerenciar Curso'...")
        time.sleep(2)
        
        gerenciar_curso_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//button[text()='Gerenciar Curso'])[2]"))
        )

        gerenciar_curso_btn.click()
        print("✅ Clicado em 'Gerenciar Curso' no primeiro curso disponível.")
        time.sleep(2)

        print("5️⃣ Clicando na aba 'AVALIAÇÕES'...")
        avaliacoes_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button:nth-child(6)")) 
        )
        avaliacoes_link.click()
        print("✅ Clicado na aba 'AVALIAÇÕES' (Continua para a lista de provas).")
        
    
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(1)

        print("6️⃣ Aguardando a lista de avaliações carregar...")
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Avaliações Cadastradas')]"))
        )
        print("✅ Lista carregada. Procurando botão 'ATRIBUIR NOTA'...")

        # Espera o botão aparecer no DOM
        atribuir_nota_btn = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//button[contains(., 'Atribuir Nota')]"
            ))
        )

        # Aguarda overlay sumir (caso exista)
        try:
            wait.until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBackdrop-root"))
            )
        except:
            pass

        # Rola o botão para o centro
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", atribuir_nota_btn)
        time.sleep(0.7)

        # Força clique real (dispatchEvent)
        driver.execute_script("""
        const button = arguments[0];
        const evt = new MouseEvent('click', {bubbles: true, cancelable: true, view: window});
        button.dispatchEvent(evt);
        """, atribuir_nota_btn)

        print("✅ Clique REAL executado no 'ATRIBUIR NOTA'.")
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(1)

    except Exception as e:
        print(f"\n🛑 Erro durante a execução dos passos do teste: {e}")
        print(f"URL Atual: {driver.current_url}")

if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        executar_teste_ct25(driver)
        teste_sem_atribuir_nota(driver)
        
    finally:
        time.sleep(3) 
        driver.quit()
        print("\n🚪 Teste finalizado e navegador fechado.")
