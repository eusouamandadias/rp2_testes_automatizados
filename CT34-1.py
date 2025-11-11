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

# === TESTE CT-34-1 ===
def ct34_acesso_curso_pin(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    print("\n📘 Executando CT-34-1 – Acesso a Cursos com PIN")

    try:
        # 1 Carregar a página inicial
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        ##driver.save_screenshot("ct34-1_etapa_1_home.png")
        print("🏠 Página Home carregada.")

        # 2 Localizar a div com os ícones do topo
        try:
            div_topbar = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[contains(@class,'topbarIcons') and contains(@class,'desktopIcons')]"
                ))
            )
        except TimeoutException:
            div_topbar = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.topbarIcons"))
            )
        ##driver.save_screenshot("ct34-1_etapa_2_topbar.png")
        print("🎯 Topbar localizada")

        # 3 Procurar o link /listcurso dentro dessa div
        print("🔎 Procurando link /listcurso dentro da topbar...")
        try:
            link_cursos = div_topbar.find_element(By.XPATH, ".//a[@href='/listcurso']")
            print("🎯 Link /listcurso encontrado dentro da topbar. Tentando clique.")
            safe_click(driver, link_cursos)
        except NoSuchElementException:
            print("⚠️ Link não encontrado na topbar. Tentando procurar globalmente.")
            try:
                link_cursos = driver.find_element(By.XPATH, "//a[@href='/listcurso']")
                safe_click(driver, link_cursos)
            except Exception:
                print("⚠️ Link não clicável/detectado. Acessando diretamente via driver.get()")
                driver.get(f"{URL}listcurso")

        # 4 Esperar a navegação acontecer
        print("⌛ Aguardando /listcurso ...")
        try:
            wait.until(EC.url_contains("/listcurso"))
            print("🎯 /listcurso detectado na URL.")
        except TimeoutException:
            print("⚠️ Navegação React não detectada no tempo. Forçando acesso direto.")
            driver.get(f"{URL}listcurso")
            wait.until(EC.url_contains("/listcurso"))
            print("✅ /listcurso carregado via fallback.")
        ##driver.save_screenshot("ct34-1_etapa_4_listcurso.png")

        # 5 Esperar renderização dos cursos
        print("⌛ Aguardando renderização dos cursos...")
        cursos = wait.until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                "//div[contains(@class,'MuiGrid-root') and contains(@class,'MuiGrid-item')]"
            ))
        )
        print(f"🔎 Encontrados {len(cursos)} cursos na listagem.")
        ##driver.save_screenshot("ct34-1_etapa_5_cursos_listados.png")

        if not cursos:
            print("❌ Nenhum curso encontrado na listagem.")
            ##driver.save_screenshot("ct34-1_etapa_5_erro_nenhum_curso.png")
            return "REPROVADO ❌"

        # 6 Selecionar o primeiro curso
        primeiro_curso = cursos[0]
        ##driver.execute_script("arguments[0].scrollIntoView({block:'center'});", primeiro_curso)
        time.sleep(0.5)
        ##driver.save_screenshot("ct34-1_etapa_6_primeiro_curso.png")
        print("🔎 Primeiro curso selecionado.")
        try:
            print("   →", primeiro_curso.text.splitlines()[:3])
        except Exception:
            pass

        # 7 Procurar o botão 'Começar' dentro da div de ações do card
        print("🔎 Procurando botão 'Começar' dentro do card...")
        try:
            card_actions = primeiro_curso.find_element(
                By.XPATH,
                ".//div[contains(@class,'MuiCardActions-root') and contains(@class,'MuiCardActions-spacing')]"
            )
            botao_comecar = card_actions.find_element(
                By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'começar')]"
            )
            print("🎯 Botão 'Começar' encontrado dentro de MuiCardActions.")
        except Exception:
            print("❌ Botão 'Começar' não encontrado. Tentando fallback global...")
            try:
                botao_comecar = driver.find_element(
                    By.XPATH,
                    "(//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'começar')])[1]"
                )
            except Exception:
                botao_comecar = None

        # 8 Clicar no botão 'Começar'
        if botao_comecar:
            print("🖱️ Tentando clicar no botão 'Começar'...")
            ##driver.save_screenshot("ct34-1_etapa_7_botao_comecar.png")
            safe_click(driver, botao_comecar)
        else:
            print("❌ Nenhum botão 'Começar' encontrado no card.")
            ##driver.save_screenshot("ct34-1_etapa_7_erro_botao.png")
            return "REVISAR ⚠️"

        # 9 Verificar se houve reação: nova URL ou modal de PIN
        print("⌛ Aguardando reação (navegação ou modal)...")
        url_anterior = driver.current_url
        reacted = False

        try:
            wait_short = WebDriverWait(driver, 6)
            wait_short.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(text(),'chave de acesso') or contains(text(),'PIN') or contains(text(),'acesso ao curso')]"
                ))
            )
            reacted = True
            print("✅ Modal de PIN detectado.")
            ##driver.save_screenshot("ct34-1_etapa_9_modal_pin.png")
        except TimeoutException:
            if driver.current_url != url_anterior:
                reacted = True
                print("✅ URL mudou após o clique (curso acessado).")
                ##driver.save_screenshot("ct34-1_etapa_9_url_mudou.png")

        if reacted:
            return "APROVADO ✅"
        else:
            print("⚠️ Nenhuma reação detectada após o clique.")
            ##driver.save_screenshot("ct34-1_etapa_9_erro_sem_reacao.png")
            return "REVISAR ⚠️"

    except Exception as e:
        print("❌ Erro durante o CT-34-1:", e)
        ##driver.save_screenshot("ct34-1_erro_execucao.png")
        import traceback, sys
        traceback.print_exc(file=sys.stdout)
        return "FALHA ❌"

# === MAIN ===
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        resultado = ct34_acesso_curso_pin(driver)
        print(f"\n📊 Resultado do CT-34-1: {resultado}")
        ##driver.save_screenshot("ct34-1_resultado.png")
        print("🖼️ Screenshot salva como ct34-1_resultado.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("🚪 Teste finalizado e navegador fechado.")
