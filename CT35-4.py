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

# === Configuração do Selenium ===
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def safe_click(driver, element):
    """Tenta clicar de forma segura, com fallback via JavaScript."""
    try:
        element.click()
    except (ElementClickInterceptedException, ElementNotInteractableException, WebDriverException):
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", element)

# === TESTE CT-35-1 ===
def ct35_acesso_curso(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    print("\n📘 Executando CT-35-4 – Acesso a Cursos sem PIN por Usuário não Autenticado")

    try:
        # 1 Acessar página inicial
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        ##driver.save_screenshot("ct35-4_etapa_1_home.png")
        print("🏠 Página Home carregada.")

        # 2 Acessar /listcurso
        time.sleep(3)
        driver.get(f"{URL}listcurso")
        wait.until(EC.url_contains("/listcurso"))
        ##driver.save_screenshot("ct35-4_etapa_2_listcurso.png")
        print("✅ Página de cursos carregada.")

        # 3 Renderizar cursos
        cursos = wait.until(EC.presence_of_all_elements_located((
            By.XPATH, "//div[contains(@class,'MuiGrid-root') and contains(@class,'MuiGrid-item')]"
        )))
        ##driver.save_screenshot("ct35-4_etapa_3_cursos_listados.png")
        print(f"🔎 {len(cursos)} cursos encontrados.")

        # 4 Procurar curso sem PIN
        curso_sem_pin = None
        for curso in cursos:
            try:
                curso.find_element(By.CSS_SELECTOR, "svg[data-testid='LockIcon']")
                continue  # tem cadeado, ignora
            except:
                curso_sem_pin = curso
                break

        if not curso_sem_pin:
            print("❌ Nenhum curso sem PIN encontrado.")
            ##driver.save_screenshot("ct35-4_etapa_4_erro_sem_pin.png")
            return "REPROVADO ❌"

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", curso_sem_pin)
        driver.execute_script("arguments[0].style.border='3px solid cyan';", curso_sem_pin)
        time.sleep(1)
        ##driver.save_screenshot("ct35-4_etapa_4_curso_sem_pin.png")
        print("📌 Curso sem PIN localizado.")

        # 5 Clicar no botão 'Começar'
        try:
            botao_comecar = curso_sem_pin.find_element(
                By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'começar')]"
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao_comecar)
            ##driver.save_screenshot("ct35-4_etapa_5_botao_comecar.png")
            safe_click(driver, botao_comecar)
            print("🖱️ Botão 'Começar' clicado.")
        except Exception:
            print("❌ Botão 'Começar' não encontrado.")
            ##driver.save_screenshot("ct35-4_etapa_5_erro_botao.png")
            return "REPROVADO ❌"

        # 6 Verificar se houve redirecionamento (sem modal de PIN)
        print("⌛ Verificando se houve redirecionamento...")
        url_anterior = f"{URL}listcurso"
        try:
            wait.until(lambda d: d.current_url != url_anterior)
            nova_url = driver.current_url
            ##driver.save_screenshot("ct35-4_etapa_6_url_redirecionada.png")
            print(f"✅ Redirecionado para {nova_url}.")
            return "APROVADO ✅"
        except TimeoutException:
            print("❌ A URL não mudou após clique.")
            ##driver.save_screenshot("ct35-4_etapa_6_erro_redirecionamento.png")
            return "REPROVADO ❌"

    except Exception as e:
        print("❌ Erro durante o CT-35-4:", e)
        ##driver.save_screenshot("ct35-4_erro_execucao.png")
        traceback.print_exc()
        return "FALHA ❌"

# === MAIN ===
if __name__ == "__main__":
    driver = setup_driver()
    try:
        resultado = ct35_acesso_curso(driver)
        print(f"\n📊 Resultado do CT-35-4: {resultado}")
        ##driver.save_screenshot("ct34-4_resultado.png")
        print("🖼️ Screenshot salva como ct35-4_resultado.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("🚪 Teste finalizado e navegador fechado.")
