import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://testes.codefolio.com.br/"
TIMEOUT = 10


# === Configuração Selenium ===
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


# === TESTE CT-33-4 ===
def ct33_recomendacao_usuario_nao_autenticado(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    print("\n📘 Executando CT-33-4 – Recomendação Visível para Usuários não Autenticados")

    try:
        # 1 Acessar o site
        print(f"🌐 Acessando: {URL}")
        driver.get(URL)
        ##driver.save_screenshot("ct33-4_etapa_1_home.png")

        # 2 Esperar a página carregar completamente
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("🏠 Página Home carregada.")
        time.sleep(3)
        ##driver.save_screenshot("ct33-4_etapa_2_body_renderizado.png")

        # 3 Procurar por cursos recomendados
        cursos = driver.find_elements(
            By.CSS_SELECTOR,
            "div.MuiGrid-root.MuiGrid-item.css-tolxbf"
        )
        ##driver.save_screenshot("ct33-4_etapa_3_cursos_recomendados.png")

        if len(cursos) == 0:
            print("❌ Nenhum curso recomendado visível.")
            ##driver.save_screenshot("ct33-4_etapa_3_erro_nenhum_curso.png")
            return "REPROVADO ❌"

        print(f"✅ Foram encontrados {len(cursos)} cursos recomendados.")

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
            print("⚠️ Nenhum curso sem PIN encontrado.")
            ##driver.save_screenshot("ct33-4_etapa_4_erro_sem_pin.png")
            return "REVISAR ⚠️"

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", curso_sem_pin)
        ##driver.save_screenshot("ct33-4_etapa_4_curso_sem_pin.png")

        # 5 Clicar no botão "Acessar"
        try:
            botao_acessar = curso_sem_pin.find_element(
                By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'acessar')]"
            )
            ##driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao_acessar)
            time.sleep(1)
            ##driver.save_screenshot("ct33-4_etapa_5_botao_acessar.png")
            botao_acessar.click()
            print("🖱️ Botão 'Acessar' clicado.")
        except:
            print("❌ Botão 'Acessar' não encontrado.")
            ##driver.save_screenshot("ct33-4_etapa_5_erro_botao.png")
            return "REPROVADO ❌"

        # 6 Validar redirecionamento pela mudança de URL
        url_antes = URL
        ##driver.save_screenshot("ct33-4_etapa_6_url_antes.png")
        wait.until(lambda d: d.current_url != url_antes)
        nova_url = driver.current_url
        ##driver.save_screenshot("ct33-4_etapa_6_url_depois.png")
        print(f"📄 URL após clique: {nova_url}")

        if nova_url != url_antes:
            print("✅ Curso acessado com sucesso.")
            return "APROVADO ✅"
        else:
            print("❌ A URL não mudou após o clique.")
            return "REPROVADO ❌"

    except Exception as e:
        print("⚠️ Erro durante a execução do caso de teste:", e)
        ##driver.save_screenshot("ct33-4_erro_execucao.png")
        return "FALHA ❌"

# === MAIN ===
if __name__ == "__main__":
    driver = setup_driver()
    try:
        resultado = ct33_recomendacao_usuario_nao_autenticado(driver)
        print(f"\n📊 Resultado do CT-33-4: {resultado}")
        ##driver.save_screenshot("ct33-4_resultado.png")
        print("🖼️ Screenshot salva como ct33-4_resultado.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("🚪 Teste finalizado e navegador fechado.")
