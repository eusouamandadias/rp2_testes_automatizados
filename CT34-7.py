import json
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)

URL = "https://testes.codefolio.com.br/"
TIMEOUT = 10

# === Dados de login Firebase ===
FBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
FBASE_VALUE = {
  "apiKey": "AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg",
  "appName": "[DEFAULT]",
  "createdAt": "1760400747850",
  "displayName": "Rafaela de Menezes",
  "email": "rafaeladm.aluno@unipampa.edu.br",
  "emailVerified": True,
  "isAnonymous": False,
  "lastLoginAt": "1761531481679",
  "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocLbR1GRarbRAVZlR_R9GsBpJu6bmh-dSs2l2FtlO-fW9jDmiA=s96-c",
  "providerData": [
    {
      "providerId": "google.com",
      "uid": "117536228690773112614",
      "displayName": "Rafaela de Menezes",
      "email": "rafaeladm.aluno@unipampa.edu.br",
      "phoneNumber": None,
      "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocLbR1GRarbRAVZlR_R9GsBpJu6bmh-dSs2l2FtlO-fW9jDmiA=s96-c"
    }
  ],
  "stsTokenManager": {
    "accessToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NTEzMjA5OWFkNmJmNjEzODJiNmI0Y2RlOWEyZGZlZDhjYjMwZjAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiUmFmYWVsYSBkZSBNZW5lemVzIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xiUjFHUmFyYlJBVlpsUl9SOUdzQnBKdTZibWgtZFNzMmwyRnRsTy1mVzlqRG1pQT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9yZWFjdC1uYS1wcmF0aWNhIiwiYXVkIjoicmVhY3QtbmEtcHJhdGljYSIsImF1dGhfdGltZSI6MTc2MTUzMTQ4MSwidXNlcl9pZCI6ImRGYldIM3VKakpYTzhzOTFIQjZEUVVTRWZEUjIiLCJzdWIiOiJkRmJXSDN1SmpKWE84czkxSEI2RFFVU0VmRFIyIiwiaWF0IjoxNzYyMjg2NDIyLCJleHAiOjE3NjIyOTAwMjIsImVtYWlsIjoicmFmYWVsYWRtLmFsdW5vQHVuaXBhbXBhLmVkdS5iciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTE3NTM2MjI4NjkwNzczMTEyNjE0Il0sImVtYWlsIjpbInJhZmFlbGFkbS5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.L93dnXl50tNdRAxUtQV_LTfb-mL1I-swTGgJlxuR8HVVbAgapRXMPoUsALrTz-FPbUWceeN6z6l7hypGz8rw0c87UnqZb8EF9vdBQM5ihbtcYJXvXUI5lfannS3N0ZpSoNSBE6mHn8giktyVCrkGEb5UNGUup8S8zlpT7OPIKlDRzGMH-OP4IehdfbDqjsmWEfKgnrSMCAbeDNo8L9eb5e0nEXoBmNGlCZEIV5ppSpYltM38N4JngeiDjxsa_YnaWa_4gOM9ZIBtpDTHHemxqpVDQP8fp1WrVgAVTAexpDlz4EeuNCXxLocGfMZ2LLn07UI7vk-7gWwhxQ7fmtpn_Q",
    "expirationTime": 1762290031864,
    "refreshToken": "AMf-vBy-rQM84RuM8yunDGZs3SSeN5n4L5BV9dpIgKSOZIVuGI_fqOc7gs6RqN5EIIDSBaz78PYmg0XizxSKJK1DxZUH_64trN198at5H_tVVufJBGHVp6oXFcsoDqC6HaisGMKK5XsigXXFZIPHjejkQD-3boiCTJuR-eJKKfeuNO9-nJxeCSrKBrPkuZ24hvroTc8u21r-VBPhfEXOzww_l5xWp0XH3YAp5u2U6Wux-rTV-6NZ1n4yHmEtXFh95DdVQyhTEu8iJQyz_c6Jn98bOz7THWZhvAvUDqk5IU7l9UmP3afnlomXnffT3qtTrtkD57cOJD32FxmC97UaLj0Y6QSHQxUAml67HRZWT4-pFh0Ir7GqTIxM8CxFzunY5xg_5R6gH34rFV43j0Ggz5xIsF-wzyoPQd1E6-9oFP2VhLXHDR40CzRMwaVUwYEYOwCukGrYjPGnc7KJHMlh0G38uhN8eyPTVA"
  },
  "uid": "dFbWH3uJjJXO8s91HB6DQUSEfDR2"
}


# === Configuração do Selenium ===
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


# === Login Firebase ===
def login_firebase(driver):
    driver.get(URL)
    time.sleep(1)
    json_str = json.dumps(FBASE_VALUE)
    script = f"window.localStorage.setItem({json.dumps(FBASE_KEY)}, `{json_str}`);"
    driver.execute_script(script)
    driver.execute_script("window.location.reload();")
    time.sleep(4)
    print("✅ Usuário autenticado via Firebase.")


def safe_click(driver, element):
    """Tenta clicar de forma segura, com fallback via JavaScript."""
    try:
        element.click()
    except (ElementClickInterceptedException, ElementNotInteractableException, WebDriverException):
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", element)


# === TESTE CT-34-7===
def ct34_fechar_janela_pin(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    print("\n📘 Executando CT-34-7 – Fechar Janela do PIN Clicando Fora da Área da Mesma")

    try:
        # 1 Acessar página inicial
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.save_screenshot("ct34-7_etapa_1_home.png")
        print("🏠 Página Home carregada.")

        # 2 Localizar topbar e acessar /listcurso
        try:
            div_topbar = wait.until(EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class,'topbarIcons') and contains(@class,'desktopIcons')]"
            )))
            link_cursos = div_topbar.find_element(By.XPATH, ".//a[@href='/listcurso']")
            safe_click(driver, link_cursos)
            print("🎯 Topbar localizada.")
        except Exception:
            print("⚠️ Link não encontrado ou não clicável. Acessando diretamente.")
            driver.get(f"{URL}listcurso")
        driver.save_screenshot("ct34-7_etapa_2_listcurso.png")

        # 3 Aguardar carregamento da página
        wait.until(EC.url_contains("/listcurso"))
        driver.save_screenshot("ct34-7_etapa_3_listcurso_carregado.png")
        print("✅ Página carregada.")

        # 4 Localizar container principal de cursos
        print("⌛ Localizando container principal de cursos...")
        container = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.css-1eikg3m"
        )))
        driver.save_screenshot("ct34-7_etapa_4_container_localizado.png")
        print("✅ Container localizado.")

        # 5 Selecionar o primeiro curso
        print("⌛ Selecionando o primeiro curso...")
        cursos = container.find_elements(
            By.CSS_SELECTOR,
            "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.MuiCard-root"
        )

        if not cursos:
            print("❌ Nenhum curso encontrado.")
            driver.save_screenshot("ct34-7_etapa_5_erro_nenhum_curso.png")
            return "REPROVADO ❌"

        primeiro_curso = cursos[0]
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", primeiro_curso)
        driver.execute_script("arguments[0].style.border='3px solid cyan';", primeiro_curso)
        driver.save_screenshot("ct34-7_etapa_5_primeiro_curso.png")
        print("🎯 Primeiro curso localizado e destacado.")

        # 6 Procurar e clicar no botão 'Começar'
        print("🔎 Procurando botão 'Começar' dentro do card...")
        try:
            card_actions = primeiro_curso.find_element(By.XPATH,
                ".//div[contains(@class,'MuiCardActions-root') and contains(@class,'MuiCardActions-spacing')]")
            botao_comecar = card_actions.find_element(By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'começar')]")
            driver.save_screenshot("ct34-7_etapa_6_botao_comecar.png")
            print("🖱️ Botão 'Começar' encontrado. Clicando...")
            safe_click(driver, botao_comecar)
        except Exception:
            print("❌ Botão 'Começar' não encontrado.")
            driver.save_screenshot("ct34-7_etapa_6_erro_botao.png")
            return "REVISAR ⚠️"

        # 7 Esperar modal de PIN
        print("⌛ Aguardando modal de PIN aparecer...")
        try:
            modal_pin = wait.until(EC.presence_of_element_located((
                By.XPATH, "//*[contains(text(),'PIN') or contains(text(),'chave de acesso') or contains(text(),'acesso ao curso')]"
            )))
            driver.save_screenshot("ct34-7_etapa_7_modal_pin.png")
            print("✅ Modal de PIN detectado.")
        except TimeoutException:
            print("⚠️ Nenhum modal detectado após clicar em 'Começar'.")
            driver.save_screenshot("ct34-7_etapa_7_erro_modal.png")
            return "REVISAR ⚠️"

        # 8 Clicar no backdrop do modal para fechá-lo
        print("🖱️ Clicando no backdrop (fora do modal) para fechar...")
        try:
            backdrop = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "div.MuiBackdrop-root.MuiModal-backdrop.css-14dl35y"
            )))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", backdrop)
            time.sleep(0.5)
            driver.save_screenshot("ct34-7_etapa_8_backdrop_localizado.png")
            safe_click(driver, backdrop)
            print("✅ Clique no backdrop executado com sucesso.")
        except TimeoutException:
            print("❌ Backdrop não encontrado.")
            driver.save_screenshot("ct34-7_etapa_8_erro_backdrop.png")
            return "REVISAR ⚠️"

        # 9 Verificar se o modal foi fechado
        print("⌛ Verificando se o modal foi fechado...")
        time.sleep(2)
        modal_aberto = len(driver.find_elements(
            By.XPATH,
            "//*[contains(text(),'PIN') or contains(text(),'chave de acesso') or contains(text(),'acesso ao curso')]"
        )) > 0

        if modal_aberto:
            print("❌ Modal de PIN ainda aberto após clique no backdrop.")
            driver.save_screenshot("ct34-7_etapa_9_modal_ainda_aberto.png")
            return "REPROVADO ❌"
        else:
            print("✅ Modal fechado com sucesso após clique fora.")
            driver.save_screenshot("ct34-7_etapa_9_modal_fechado.png")
            return "APROVADO ✅"

    except Exception as e:
        print("❌ Erro durante o CT-34-7:", e)
        driver.save_screenshot("ct34-7_erro_execucao.png")
        traceback.print_exc()
        return "FALHA ❌"

# === MAIN ===
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        resultado = ct34_fechar_janela_pin(driver)
        print(f"\n📊 Resultado do CT-34-7: {resultado}")
        driver.save_screenshot("ct34-7_resultado.png")
        print("🖼️ Screenshot salva como ct34-7_resultado.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("🚪 Teste finalizado e navegador fechado.")
