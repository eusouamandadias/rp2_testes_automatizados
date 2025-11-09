import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

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

# === Configuração Selenium ===
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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
    print("✅ Usuário autenticado via Firebase.")

# === TESTE CT-33-2 ===
def ct33_abertura_correta_curso_recomendado(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    print("\n📘 Executando CT-33-2 – Abertura Correta do Curso Recomendado")

    try:
        # 1 Garantir que a Home está carregada
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.save_screenshot("ct33-2_etapa_1_home.png")
        print("🏠 Página Home carregada.")

        # 2 Localizar container de cursos recomendados
        div_cursos = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-direction-xs-column.css-279f3v"
            ))
        )
        cursos = div_cursos.find_elements(By.XPATH, ".//div[contains(@class,'MuiPaper-root')]")
        driver.save_screenshot("ct33-2_etapa_2_container.png")
        print(f"🔍 {len(cursos)} cursos recomendados detectados.")

        # 3 Procurar curso sem PIN
        curso_sem_pin = None
        for curso in cursos:
            try:
                curso.find_element(By.CSS_SELECTOR, "svg[data-testid='LockIcon']")
                continue  # tem cadeado, ignora
            except:
                curso_sem_pin = curso
                break

        if not curso_sem_pin:
            print("⚠️ Nenhum curso sem PIN encontrado.")
            driver.save_screenshot("ct33-2_etapa_3_erro_sem_pin.png")
            return "REVISAR ⚠️"

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", curso_sem_pin)
        driver.save_screenshot("ct33-2_etapa_3_curso_sem_pin.png")

        # 4 Capturar nome do curso
        nome_elementos = curso_sem_pin.find_elements(By.XPATH, ".//h6 | .//h5 | .//h4")
        nome_curso = ""
        for el in nome_elementos:
            texto = el.text.strip()
            if texto:
                nome_curso = texto
                break

        if not nome_curso:
            print("⚠️ Não foi possível capturar o nome do curso.")
            driver.save_screenshot("ct33-2_etapa_4_erro_nome.png")
            return "REVISAR ⚠️"

        print(f"📌 Curso selecionado: '{nome_curso}'")

        # 5 Clicar no botão "Acessar"
        try:
            botao_acessar = curso_sem_pin.find_element(
                By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'acessar')]"
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao_acessar)
            time.sleep(1)
            driver.save_screenshot("ct33-2_etapa_5_botao_acessar.png")
            botao_acessar.click()
            print("🖱️ Botão 'Acessar' clicado.")
        except:
            print("❌ Botão 'Acessar' não encontrado.")
            driver.save_screenshot("ct33-2_etapa_5_erro_botao.png")
            return "REPROVADO ❌"

        # 6 Esperar redirecionamento
        wait.until(EC.url_changes(URL))
        nova_url = driver.current_url
        time.sleep(5)
        driver.save_screenshot("ct33-2_etapa_6_url_redirecionada.png")
        print(f"📄 Página do curso aberta: {nova_url}")

        # 7 Validar título do curso
        titulo_div = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.MuiBox-root.css-13lzww4"))
        )
        titulo_texto = titulo_div.text.strip()
        driver.save_screenshot("ct33-2_etapa_7_titulo.png")
        print(f"🔖 Título exibido: '{titulo_texto}'")

        if titulo_texto.lower() in nome_curso.lower() or nome_curso.lower() in titulo_texto.lower():
            print("✅ Curso aberto corresponde ao curso clicado.")
            return "APROVADO ✅"
        else:
            print(f"⚠️ Curso aberto diferente: card='{nome_curso}', página='{titulo_texto}'")
            return "REVISAR ⚠️"

    except Exception as e:
        print("❌ Erro durante execução:", e)
        driver.save_screenshot("ct33-2_erro_execucao.png")
        return "FALHA ❌"

# === MAIN ===
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        resultado = ct33_abertura_correta_curso_recomendado(driver)
        print(f"\n📊 Resultado do CT-33-2: {resultado}")
        driver.save_screenshot("ct33-2_resultado.png")
        print("🖼️ Screenshot salva como ct33-2_resultado.png")
    finally:
        time.sleep(5)
        driver.quit()
        print("🚪 Teste finalizado e navegador fechado.")
