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
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    WebDriverException
)

URL = "https://testes-codefolio.web.app/"
TIMEOUT = 10

# === Dados de login Firebase ===
FBASE_KEY = "firebase:authUser:AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co:[DEFAULT]"
FBASE_VALUE = {
  "apiKey": "AIzaSyAPX5N0upfNK5hYS2iQzof-XNTcDDYL7Co",
  "appName": "[DEFAULT]",
  "createdAt": "1763434703970",
  "displayName": "Rafaela de Menezes",
  "email": "rafaeladm.aluno@unipampa.edu.br",
  "emailVerified": True,
  "isAnonymous": False,
  "lastLoginAt": "1763693536574",
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
    "accessToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ1YTZjMGMyYjgwMDcxN2EzNGQ1Y2JiYmYzOWI4NGI2NzYxMjgyNjUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiUmFmYWVsYSBkZSBNZW5lemVzIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xiUjFHUmFyYlJBVlpsUl9SOUdzQnBKdTZibWgtZFNzMmwyRnRsTy1mVzlqRG1pQT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS90ZXN0ZXMtY29kZWZvbGlvIiwiYXVkIjoidGVzdGVzLWNvZGVmb2xpbyIsImF1dGhfdGltZSI6MTc2MzY5MzUzNiwidXNlcl9pZCI6Ino2bU5sTG9nY0liYzlBbTdYTHFDUEdiVFRqWjIiLCJzdWIiOiJ6Nm1ObExvZ2NJYmM5QW03WExxQ1BHYlRUaloyIiwiaWF0IjoxNzYzODQyOTcxLCJleHAiOjE3NjM4NDY1NzEsImVtYWlsIjoicmFmYWVsYWRtLmFsdW5vQHVuaXBhbXBhLmVkdS5iciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTE3NTM2MjI4NjkwNzczMTEyNjE0Il0sImVtYWlsIjpbInJhZmFlbGFkbS5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.o5q4DpSCp95oC4cpnidbuCYRCrhT5wNo8MTm7sJgLpCthpCZZGROGp9qXQG2uJkj_Cinj2T8VpqDpCAvlHxpAOpKKEbXmp-QDHH_DZvwvUpSsye7ihcEo4BsoRYHEinSLK2BCqeVe1E9Ywb8kK99RShuE8n4_QlV2LEZ7I87XNf2-whjPtx-GCMApCdojsIJnsG9p_JNVmE4D9zFwRPfFdnaRe7LfjrWphttVYTzRmIC7zgaqKKj_ODOdD-Pn-PyT1j-zHYpOcrHHKIJ3q5anxVbZZnAwC8dS6zmokSaakGYHjh8GFYt7XDQY9CqSzGfoz2enZodJhqjDA7K9hUGSA",
    "expirationTime": 1763846579209,
    "refreshToken": "AMf-vBxMezIyDaq12GobE9hDuHBCCNeIu-yyVhHD44Ua9AX6PL44kqpsGsRZkVEbkl0UWFyv27vbBFWxI58AkOsoZDuCADn_8q075or2HiO2-3fowbWtehJiYdEcVDFKUdSIfZLeLtx_yXCkW6BUEXjxzfvCREtR-6tJHwrOvta2UhuzrtC2XzQ5XotKtQ_gb-GwQch89nttd09UVCnB5wgaPzQHGKa3dL0SvMmFp-0qZ9HOLGgTmEvUY6CHf-pdocFLgEAVHqgDZAwdkcxusTB1GMAB4lFakbvh8YhtaQWk7CGm3nGAvRxFGokzEPlSenj9FPwSbss2DzZbAZ2Fx6s8Ej54cumaY6jLtTSVPYMH_LU7NFf1gWhrX-EB6lxaGM0jn6CRCwzt4jS3p9sMrXW7xkuU4kT8QkREp94J6RPxnvMz6QQoy9xkd3194JnNQJZaFffASzlHIIKyu2-QLtHlKiw6oZ8Ezg"
  },
  "uid": "z6mNlLogcIbc9Am7XLqCPGbTTjZ2"
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

# === TESTE CT-36-2 ===
def ct36_visualizacao_ranking_quiz_pergunta_personalizada(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    print("\n📘 Executando CT-36-2 – Visualizar Ranking após Realizar Pergunta Personalizada")

    try:
        # 1 Acessar página inicial
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.save_screenshot("ct36-2_pagina_home.png")
        print("🏠 Página Home carregada.")

        # 2 Acessar /listcurso
        driver.get(f"{URL}listcurso")
        wait.until(EC.url_contains("/listcurso"))
        driver.save_screenshot("ct36-2_pagina_cursos.png")
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
            driver.save_screenshot("ct36-2_aba_concluidos.png")
            print("🖱️ Aba 'Concluídos' clicada.")
        except Exception:
            driver.save_screenshot("ct36-2_erro_aba_concluidos.png")
            print("❌ Aba 'Concluídos' não encontrada.")
            return "REVISAR ⚠️"

        # 4 Selecionar o primeiro curso da aba "Concluídos"
        cursos_concluidos = wait.until(EC.presence_of_all_elements_located((
            By.XPATH, "//div[contains(@class,'MuiGrid-root') and contains(@class,'MuiGrid-item')]"
        )))
        if not cursos_concluidos:
            driver.save_screenshot("ct36-2_erro_sem_cursos.png")
            print("❌ Nenhum curso encontrado na aba 'Concluídos'.")
            return "REPROVADO ❌"

        curso_selecionado = cursos_concluidos[0]
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", curso_selecionado)
        driver.execute_script("arguments[0].style.border='3px solid orange';", curso_selecionado)
        driver.save_screenshot("ct36-2_primeiro_curso.png")
        print("📌 Primeiro curso da aba 'Concluídos' selecionado.")

        # 5 Clicar no botão "Ver Curso"
        try:
            botao_acesso = curso_selecionado.find_element(
                By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ver curso')]"
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao_acesso)
            safe_click(driver, botao_acesso)
            driver.save_screenshot("ct36-2_5_botao_ver_curso.png")
            print("🖱️ Botão 'Ver Curso' clicado).")
        except Exception:
            driver.save_screenshot("ct36-2_erro_botao_ver_curso.png")
            print("❌ Botão 'Ver Curso' não encontrado.")
            return "REPROVADO ❌"

        # 6 Abrir Quiz Gigi
        time.sleep(3)
        try:
            botao_abrir_quiz = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@title,'Abrir Quiz Gigi')]")
            ))
            botao_abrir_quiz.click()
            driver.save_screenshot("ct36-2_botao_quiz_gigi.png")
            print("🖱️ Botão 'Quiz Gigi' clicado.")
        except Exception:
            driver.save_screenshot("ct36-2_erro_botao_quiz_gigi.png")
            print("❌ Não foi possível encontrar o botão 'Quiz Gigi'.")
            return "REPROVADO ❌"

        # 7 Clicar no botão "Pergunta Personalizada"
        try:
            print("🔎 Procurando botão 'Pergunta Personalizada'")
            botao_resumo = wait.until(EC.presence_of_element_located((
                    By.XPATH, "//button[@aria-label='Pergunta Personalizada']"
            )))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao_resumo)
            safe_click(driver, botao_resumo)
            driver.save_screenshot("ct36-1_botao_pergunta_personalizada.png")
            time.sleep(5)
            print("🖱️ Botão 'Pergunta Personalizada' clicado.")
        except Exception:
                driver.save_screenshot("ct36-1_erro_botao_pergunta_personalizada.png")
                print("❌ Botão 'Pergunta Personalizada' não encontrado.")
                return "REPROVADO ❌"

        # 8 Clicar no botão "Ranking do Quiz"
        try:
            time.sleep(2)
            print("🔎 Procurando botão 'Ranking do Quiz'")
            botao_ranking = wait.until(EC.presence_of_element_located((
                By.XPATH, "//button[@aria-label='Ranking do Quiz']"
            )))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao_ranking)
            safe_click(driver, botao_ranking)
            driver.save_screenshot("ct36-2_botao_ranking.png")
            time.sleep(2)
            print("🖱️ Botão 'Ranking do Quiz' clicado.")
        except Exception:
            driver.save_screenshot("ct36-2_erro_botao_ranking.png")
            print("❌ Botão 'Ranking do Quiz' não encontrado.")
            return "REPROVADO ❌"
            
        # 9 Voltar para a tela de pergunta personalizada utilizando a tecla ESC 
        try:
            time.sleep(3)
            print("⌨️ Apertando a tecla 'ESC'")
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(2)
        except Exception:
                driver.save_screenshot("ct36-1_erro_tecla_ESC.png")
                print("❌ Tecla 'ESC' não encontrada.")
                return "REPROVADO ❌"
            
        # 10 Clicar no botão "Voltar ao modo normal"
        try:
            time.sleep(3)
            print("🔎 Procurando botão 'Voltar ao modo normal'")
            botao_modo_normal = wait.until(EC.presence_of_element_located((
                    By.XPATH, "//button[@aria-label='Voltar ao modo normal']"
            )))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao_modo_normal)
            safe_click(driver, botao_modo_normal)
            driver.save_screenshot("ct36-1_botao_modo_normal.png")
            time.sleep(2)
            print("🖱️ Botão 'Voltar ao modo normal' clicado.")
            return "APROVADO ✅"
        except Exception:
                driver.save_screenshot("ct36-1_erro_botao_modo_normal.png")
                print("❌ Botão 'Voltar ao modo normal' não encontrado.")
                return "REPROVADO ❌"

    except Exception as e:
        driver.save_screenshot("ct36-2_falha.png")
        print("❌ Erro durante o CT-36-2:", e)
        traceback.print_exc()
        return "FALHA ❌"

        
# === MAIN ===
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        resultado= ct36_visualizacao_ranking_quiz_pergunta_personalizada(driver)
        print(f"\n📊 Resultado do CT-36-2: {resultado}")
        ##driver.save_screenshot("ct36-2_resultado.png")
        print("🖼️ Screenshot salva como ct36-2_resultado.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("🚪 Teste finalizado e navegador fechado.")