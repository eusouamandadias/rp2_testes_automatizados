import json
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    TimeoutException,
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

# === TESTE CT-35-3 ===
def ct35_historico_curso_concluido(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    print("\n📘 Executando CT-35-3 – Histórico de Cursos Concluídos")

    try:
        # 1 Acessar página inicial
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("🏠 Página Home carregada.")

        # 2 Acessar /listcurso
        driver.get(f"{URL}listcurso")
        wait.until(EC.url_contains("/listcurso"))
        print("✅ Página de cursos carregada.")
        
        # 3 Clicar na aba "EM ANDAMENTO"
        try:
            abas_container = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "div.MuiTabs-flexContainer.MuiTabs-centered"
            )))
            aba_em_andamento = abas_container.find_element(By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'em andamento')]"
            )
            safe_click(driver, aba_em_andamento)
            time.sleep(2)
            print("🖱️ Aba 'EM ANDAMENTO' clicada.")
        except Exception:
            print("⚠️ Aba 'EM ANDAMENTO' não encontrada.")
            return "REVISAR ⚠️"
        
        # 4 Renderizar cursos
        cursos = wait.until(EC.presence_of_all_elements_located((
            By.XPATH, "//div[contains(@class,'MuiGrid-root') and contains(@class,'MuiGrid-item')]"
        )))
        print(f"🔎 {len(cursos)} cursos encontrados.")

        # 5 Procurar curso com nome "React Native Básico"
        curso_alvo = None
        for curso in cursos:
            if "React Native Básico" in curso.text:
                curso_alvo = curso
                break

        if not curso_alvo:
            print("❌ Curso 'React Native Básico' não encontrado.")
            return "REPROVADO ❌"

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", curso_alvo)
        driver.execute_script("arguments[0].style.border='3px solid cyan';", curso_alvo)
        print("✅ Curso 'React Native Básico' localizado.")

        # 6 Clicar no botão 'Continuar'
        try:
            botao_comecar = curso_alvo.find_element(
                By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'começar')]"
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao_comecar)
            safe_click(driver, botao_comecar)
            print("🖱️ Botão 'Começar' clicado.")
        except Exception:
            print("❌ Botão 'Começar' não encontrado.")
            return "REPROVADO ❌"

        # 7 Esperar redirecionamento
        wait.until(lambda d: d.current_url != f"{URL}listcurso")
        print(f"✅ Curso acessado: {driver.current_url}")

        # 8 Procurar conteúdo dentro do card do curso
        try:
            card_conteudo = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.MuiCard-root.css-1cbjw9x"
            )))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", card_conteudo)
            driver.execute_script("arguments[0].style.border='3px solid orange';", card_conteudo)
            print("✅ Card de conteúdo localizado.")
        except TimeoutException:
            print("❌ Card de conteúdo não encontrado.")
            return "REVISAR ⚠️"

        # 9 Clicar no botão dentro do card
        try:
            botao_acao = card_conteudo.find_element(By.CSS_SELECTOR,
                "button.MuiButtonBase-root.MuiButton-root.MuiButton-containedPrimary.css-1xdgsfp"
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao_acao)
            safe_click(driver, botao_acao)
            print("✅ Botão de ação clicado com sucesso.")
        except Exception:
            print("❌ Botão de ação não encontrado dentro do card.")
            return "REVISAR ⚠️"

        # 10 Assistir vídeo do YouTube
        try:
            iframe = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//iframe[contains(@id, 'widget')]")
            ))
            driver.switch_to.frame(iframe)
            print("🎬 Iframe do YouTube selecionado.")

            botao_play = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.ytp-large-play-button")
            ))
            safe_click(driver, botao_play)
            print("▶️ Botão Play clicado.")
            time.sleep(3)

            driver.execute_script("""
                var video = document.querySelector('video');
                if (video) {
                    video.currentTime = video.duration - 2; // pula para os últimos 2 segundos
                }
            """)
            print("⏩ Vídeo avançado até o final via JavaScript.")

            driver.switch_to.default_content()

        except Exception as e:
            print("❌ Erro ao manipular vídeo do YouTube:", e)
            traceback.print_exc()
            return "REVISAR ⚠️"
        
        # 11 Clicar no botão "Fechar"
        time.sleep(3)
        botao_fechar=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.MuiButtonBase-root.MuiButton-root.MuiButton-outlined.MuiButton-outlinedPrimary.MuiButton-sizeMedium.MuiButton-outlinedSizeMedium.MuiButton-colorPrimary.MuiButton-root.MuiButton-outlined.MuiButton-outlinedPrimary.MuiButton-sizeMedium.MuiButton-outlinedSizeMedium.MuiButton-colorPrimary.css-6ddp3z")))
        safe_click(driver, botao_fechar)
        
        # 12 Clicar no botão 'Ver slide'
        try:
            container_botoes = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "div.MuiBox-root.css-rmtmmr"
            )))
            botoes = container_botoes.find_elements(By.CSS_SELECTOR, "button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.css-1xdgsfp")[1]
            time.sleep(2)
            safe_click(driver, botoes)
        except Exception:
            driver.save_screenshot("ct35_3_erro_respostas.png")
            print("❌ Não foi possível executar o ciclo de cliques e visualizar o resumo.")
            return "REPROVADO ❌"
        

        # 13 Simular finalização do curso
        print("⏳ Simulando finalização do curso...")
        time.sleep(5)
        driver.get(f"{URL}listcurso")
        wait.until(EC.url_contains("/listcurso"))
        print("🔙 Retornou para página de cursos.")

        # 14 Clicar na aba "CONCLUÍDOS"
        try:
            abas_container = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "div.MuiTabs-flexContainer.MuiTabs-centered"
            )))
            aba_concluidos = abas_container.find_element(By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'concluídos')]"
            )
            safe_click(driver, aba_concluidos)
            time.sleep(2)
            print("🖱️ Aba 'CONCLUÍDOS' clicada.")
        except Exception:
            print("⚠️ Aba 'CONCLUÍDOS' não encontrada.")
            return "REVISAR ⚠️"

        # 15 Verificar se o curso aparece na aba
        container_concluidos = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "div.MuiGrid-root.MuiGrid-container"
        )))
        cursos_concluidos = container_concluidos.find_elements(By.XPATH,
            ".//div[contains(@class,'MuiGrid-root') and contains(@class,'MuiGrid-item')]"
        )

        curso_encontrado = None
        for curso in cursos_concluidos:
            if "React Native Básico" in curso.text:
                curso_encontrado = curso
                break

        if curso_encontrado:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", curso_encontrado)
            driver.execute_script("arguments[0].style.border='3px solid lime';", curso_encontrado)
            print("✅ Curso 'React Native Básico' aparece na aba CONCLUÍDOS e foi destacado.")
            return "APROVADO ✅"
        else:
            print("❌ Curso 'Curso com vários vídeos' não aparece na aba CONCLUÍDOS.")
            return "REPROVADO ❌"

    except Exception as e:
        print("❌ Erro durante o CT-35-3:", e)
        traceback.print_exc()
        return

# === MAIN ===
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        resultado = ct35_historico_curso_concluido(driver)
        print(f"\n📊 Resultado do CT-35-3: {resultado}")
        ##driver.save_screenshot("ct34-3_resultado.png")
        print("🖼️ Screenshot salva como ct34-3_resultado.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("🚪 Teste finalizado e navegador fechado.")
