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
    WebDriverException
)

URL = "https://testes.codefolio.com.br/"
TIMEOUT = 10
PIN_CORRETO = "grupo2"  

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

# === TESTE CT-34-6 ===
def ct34_acesso_sem_autenticacao_curso_pin(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    print("\n📘 Executando CT-34-6 – Usuário não autenticado Acessa Curso com PIN")

    try:
        # 1 Acessar página inicial
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.save_screenshot("ct34-6_etapa_1_home.png")
        print("🏠 Página Home carregada.")

        # 2 Ir para /listcurso
        driver.get(f"{URL}listcurso")
        wait.until(EC.url_contains("/listcurso"))
        driver.save_screenshot("ct34-6_etapa_2_listcurso.png")
        print("✅ Página de cursos carregada.")
        
        # 3 Renderizar cursos
        cursos = wait.until(EC.presence_of_all_elements_located((
            By.XPATH, "//div[contains(@class,'MuiGrid-root') and contains(@class,'MuiGrid-item')]"
        )))
        driver.save_screenshot("ct34-6_etapa_3_cursos_listados.png")
        print(f"🔎 {len(cursos)} cursos encontrados.")
        
        # 4 Procurar curso com nome "Teste pin Grupo 2 -2"
        curso_alvo = None
        for curso in cursos:
            if "Teste pin Grupo 2 -2" in curso.text:
                curso_alvo = curso
                break

        if not curso_alvo:
            print("❌ Curso 'Teste pin Grupo 2 -2' não encontrado.")
            driver.save_screenshot("ct34-6_etapa_4_erro_curso_nao_encontrado.png")
            return "REPROVADO ❌"

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", curso_alvo)
        time.sleep(0.5)
        driver.save_screenshot("ct34-6_etapa_4_curso_encontrado.png")
        print("📌 Curso 'Teste pin Grupo 2 -2' localizado.")

        # 5 Botão 'Começar'
        try:
            card_actions = curso_alvo.find_element(By.XPATH,
                ".//div[contains(@class,'MuiCardActions-root') and contains(@class,'MuiCardActions-spacing')]")
            botao_comecar = card_actions.find_element(By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'começar')]")
        except Exception:
            try:
                botao_comecar = curso_alvo.find_element(By.XPATH,
                    ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'começar')]")
            except Exception:
                botao_comecar = None

        if botao_comecar:
            driver.save_screenshot("ct34-6_etapa_5_botao_comecar.png")
            safe_click(driver, botao_comecar)
            print("🖱️ Botão 'Começar' clicado.")
        else:
            print("❌ Botão 'Começar' não encontrado.")
            driver.save_screenshot("ct34-6_etapa_5_erro_botao.png")
            return "REVISAR ⚠️"

        # 6 Modal de PIN
        try:
            modal_pin = wait.until(EC.presence_of_element_located((
                By.XPATH, "//*[contains(text(),'chave de acesso') or contains(text(),'PIN') or contains(text(),'acesso ao curso')]"
            )))
            driver.save_screenshot("ct34-6_etapa_6_modal_pin.png")
            print("✅ Modal de PIN detectado.")
        except TimeoutException:
            driver.save_screenshot("ct34-6_etapa_6_erro_modal.png")
            return "REVISAR ⚠️"

        # 7 Inserir PIN correto
        try:
            campo_pin = wait.until(EC.presence_of_element_located((
                By.XPATH, "//input[@type='password' or @type='text' or contains(@placeholder,'PIN') or contains(@placeholder,'chave')]"
            )))
            campo_pin.clear()
            campo_pin.send_keys("123")
            driver.save_screenshot("ct34-6_etapa_7_pin_inserido.png")
            print("✅ PIN '123' inserido.")
        except TimeoutException:
            driver.save_screenshot("ct34-6_etapa_7_erro_campo.png")
            return "REVISAR ⚠️"

        # 8 Clicar em 'Enviar'
        url_antes = driver.current_url
        try:
            botao_enviar = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enviar')]"
            )))
            driver.save_screenshot("ct34-6_etapa_8_botao_enviar.png")
            safe_click(driver, botao_enviar)
            print("🖱️ Botão 'Enviar' clicado.")
        except TimeoutException:
            driver.save_screenshot("ct34-6_etapa_8_erro_botao.png")
            return "REVISAR ⚠️"

        # 9 Verificar se a URL mudou
        print("⌛ Verificando se a URL mudou após envio...")
        try:
            wait.until(lambda d: d.current_url != url_antes)
            nova_url = driver.current_url
            driver.save_screenshot("ct34-6_etapa_9_url_redirecionada.png")
            print(f"✅ Redirecionado para {nova_url}.")
            return "APROVADO ✅"
        except TimeoutException:
            print("❌ A URL não mudou após envio.")
            driver.save_screenshot("ct34-6_etapa_9_erro_redirecionamento.png")
            return "REPROVADO ❌"

    except Exception as e:
        print("❌ Erro durante o CT-34-6:", e)
        driver.save_screenshot("ct34-6_erro_execucao.png")
        traceback.print_exc()
        return "FALHA ❌"


# === MAIN ===
if __name__ == "__main__":
    driver = setup_driver()
    try:
        resultado = ct34_acesso_sem_autenticacao_curso_pin(driver)
        print(f"\n📊 Resultado do CT-34-6: {resultado}")
        driver.save_screenshot("ct34-6_resultado.png")
        print("🖼️ Screenshot salva como ct34-6_resultado.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("🚪 Teste finalizado e navegador fechado.")
