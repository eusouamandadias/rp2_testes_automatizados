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
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)
import json

URL = "https://testes.codefolio.com.br/"
TIMEOUT = 10

# === Dados de login Firebase (simulação via localStorage) ===
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

def safe_click(driver, element):
    try:
        element.click()
    except (ElementClickInterceptedException, ElementNotInteractableException, WebDriverException):
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", element)

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

# === TESTE CT-34-5 ===
def ct34_continuar_acesso_curso_liberado(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    print("\n📘 Executando CT-34-5 – Continuar Acesso ao Curso já Liberado por PIN")

    try:
        # 1 Carregar a página inicial
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        ##driver.save_screenshot("ct34-3_etapa_1_home.png")
        print("🏠 Página Home carregada.")
        
        # 2 Acessar página de cursos
        driver.get(f"{URL}listcurso")
        wait.until(EC.url_contains("/listcurso"))
        ##driver.save_screenshot("ct34-5_etapa_1_listcurso.png")
        print("✅ Página de cursos carregada.")

        # 3 Selecionar aba "EM ANDAMENTO"
        try:
            abas_container = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "div.MuiTabs-flexContainer.MuiTabs-centered.css-8enf3a"
            )))
            aba_em_andamento = abas_container.find_element(By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'em andamento')]"
            )
            safe_click(driver, aba_em_andamento)
            time.sleep(2)
            ##driver.save_screenshot("ct34-5_etapa_2_aba_em_andamento.png")
            print("🖱️ Aba 'EM ANDAMENTO' clicada com sucesso.")
        except TimeoutException:
            print("⚠️ Aba 'EM ANDAMENTO' não encontrada. Continuando na aba padrão...")
            ##driver.save_screenshot("ct34-5_etapa_2_erro_aba_em_andamento.png")

        # 4 Localizar curso protegido
        container_cursos = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.css-1eikg3m"
        )))
        cursos = container_cursos.find_elements(By.XPATH,
            ".//div[contains(@class,'MuiGrid-root') and contains(@class,'MuiGrid-item')]"
        )
        ##driver.save_screenshot("ct34-5_etapa_3_cursos_listados.png")

        curso_alvo = None
        for curso in cursos:
            try:
                lock_icon = curso.find_element(By.CSS_SELECTOR, "svg[data-testid='LockIcon']")
                if lock_icon:
                    curso_alvo = curso
                    break
            except:
                continue

        if not curso_alvo:
            print("⚠️ Nenhum curso protegido encontrado.")
            driver.save_screenshot("ct34-5_etapa_3_erro_curso_protegido.png")
            return "REVISAR ⚠️"

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", curso_alvo)
        ##driver.save_screenshot("ct34-5_etapa_3_curso_protegido_localizado.png")
        print("🔎 Curso protegido localizado.")

        # 5 Clicar em 'Continuar'
        try:
            botao_continuar = curso_alvo.find_element(By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continuar')]"
            )
            ##driver.save_screenshot("ct34-5_etapa_4_botao_continuar.png")
            safe_click(driver, botao_continuar)
            print("🖱️ Botão 'Continuar' clicado.")
        except NoSuchElementException:
            print("❌ Botão 'Continuar' não encontrado.")
            ##driver.save_screenshot("ct34-5_etapa_4_erro_botao_continuar.png")
            return "REPROVADO ❌"

        # 6 Validar acesso: verificar se não está mais em /listcurso
        time.sleep(3)
        if "/listcurso" not in driver.current_url.lower():
            ##driver.save_screenshot("ct34-5_etapa_5_url_redirecionada.png")
            print(f"✅ Teste passou: URL mudou para {driver.current_url}")
            return "APROVADO ✅"
        else:
            ##driver.save_screenshot("ct34-5_etapa_5_erro_url_nao_mudou.png")
            print(f"❌ Teste falhou: ainda está em {driver.current_url}")
            return "REPROVADO ❌"

    except Exception as e:
        print("❌ Erro durante o CT-34-5:", e)
        ##driver.save_screenshot("ct34-5_erro_execucao.png")
        traceback.print_exc()
        return "FALHA ❌"



# === MAIN ===
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver) 
        resultado = ct34_continuar_acesso_curso_liberado(driver)
        print(f"\n📊 Resultado do CT-34-5: {resultado}")
        ##driver.save_screenshot("ct34-5_resultado.png")
        print("🖼️ Screenshot salva como ct34-5_resultado.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("🚪 Teste finalizado e navegador fechado.")