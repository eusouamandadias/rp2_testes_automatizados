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

# === TESTE CT-35_2-1 ===
def ct35_visualizacao_ranking_quiz(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    print("\n📘 Executando CT-35_2-1 – Visualização de Ranking do Quiz")

    try:
        # 1 Acessar página inicial
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.save_screenshot("ct35_2-1_pagina_home.png")
        print("🏠 Página Home carregada.")

        # 2 Acessar /listcurso
        driver.get(f"{URL}listcurso")
        wait.until(EC.url_contains("/listcurso"))
        driver.save_screenshot("ct35_2-1_pagina_cursos.png")
        print("✅ Página de cursos carregada.")

        # 3 Clicar na aba "Concluídos"
        try:
            abas_container = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "div.MuiTabs-flexContainer.MuiTabs-centered"
            )))
            aba_concluidos = abas_container.find_element(By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'concluídos')]"
            )
            safe_click(driver, aba_concluidos)
            time.sleep(2)
            driver.save_screenshot("ct35_2-1_aba_concluidos.png")
            print("🖱️ Aba 'Concluídos' clicada.")
        except Exception:
            driver.save_screenshot("ct35_2-1_erro_aba_concluidos.png")
            print("❌ Aba 'Concluídos' não encontrada.")
            return "REVISAR ⚠️"

        # 4 Selecionar o primeiro curso da aba "Concluídos"
        cursos_concluidos = wait.until(EC.presence_of_all_elements_located((
            By.XPATH, "//div[contains(@class,'MuiGrid-root') and contains(@class,'MuiGrid-item')]"
        )))
        if not cursos_concluidos:
            driver.save_screenshot("ct35_2-1_erro_sem_cursos.png")
            print("❌ Nenhum curso encontrado na aba 'Concluídos'.")
            return "REPROVADO ❌"

        curso_selecionado = cursos_concluidos[0]
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", curso_selecionado)
        driver.execute_script("arguments[0].style.border='3px solid orange';", curso_selecionado)
        driver.save_screenshot("ct35_2-1_primeiro_curso.png")
        print("📌 Primeiro curso da aba 'Concluídos' selecionado.")

        # 5 Clicar no botão "Ver Curso"
        try:
            botao_acesso = curso_selecionado.find_element(
                By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ver curso')]"
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao_acesso)
            safe_click(driver, botao_acesso)
            driver.save_screenshot("ct35_5_botao_ver_curso.png")
            print("🖱️ Botão 'Ver Curso' clicado).")
        except Exception:
            driver.save_screenshot("ct35_2-1_erro_botao_ver_curso.png")
            print("❌ Botão 'Ver Curso' não encontrado.")
            return "REPROVADO ❌"

        # 6 Abrir Quiz Gigi
        time.sleep(6)
        try:
            botao_abrir_quiz = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@title,'Abrir Quiz Gigi')]")
            ))
            botao_abrir_quiz.click()
            driver.save_screenshot("ct35_2-1_botao_quiz_gigi.png")
            print("🖱️ Botão 'Quiz Gigi' clicado.")
        except Exception:
            driver.save_screenshot("ct35_2-1_erro_botao_quiz_gigi.png")
            print("❌ Não foi possível encontrar o botão 'Quiz Gigi'.")
            return "REPROVADO ❌"

        # 7 Clicar em botões aleatórios até restar apenas 1 clicável, depois clicar em "Resumo do Quiz"
        try:
            container_botoes = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "div.MuiBox-root.css-wo1xkm"
            )))
            botoes = container_botoes.find_elements(By.TAG_NAME, "button")
            time.sleep(2)

            for idx, botao in enumerate(botoes, start=1):
                safe_click(driver, botao)
                driver.save_screenshot(f"ct35_2-1_resposta_{idx}.png")
                print(f"🖱️ Resposta aleatória {idx} clicada.")
                time.sleep(2)

        # 8 Clicar no botão "Resumo do Quiz"
            try:
                print("🔎 Procurando botão 'Resumo do Quiz'")
                botao_resumo = wait.until(EC.presence_of_element_located((
                    By.XPATH, "//button[@aria-label='Resumo do Quiz']"
                )))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao_resumo)
                safe_click(driver, botao_resumo)
                driver.save_screenshot("ct35_2-1_botao_resumo.png")
                time.sleep(5)
                print("🖱️ Botão 'Resumo do Quiz' clicado.")
                return "APROVADO ✅"
            except Exception:
                driver.save_screenshot("ct35_2-1_erro_botao_resumo.png")
                print("❌ Botão 'Resumo do Quiz' não encontrado.")
                return "REPROVADO ❌"

        except Exception:
            driver.save_screenshot("ct35_2-1_erro_respostas.png")
            print("❌ Não foi possível executar o ciclo de cliques e visualizar o resumo.")
            return "REPROVADO ❌"

    except Exception as e:
        driver.save_screenshot("ct35_2-1falha.png")
        print("❌ Erro durante o CT-35_2-1:", e)
        traceback.print_exc()
        return "FALHA ❌"

        
# === MAIN ===
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        resultado = ct35_visualizacao_ranking_quiz(driver)
        print(f"\n📊 Resultado do CT-35_2-1: {resultado}")
        ##driver.save_screenshot("ct35_2-1_resultado.png")
        print("🖼️ Screenshot salva como ct35_2-1_resultado.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("🚪 Teste finalizado e navegador fechado.")