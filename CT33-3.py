import time
import traceback
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


# === TESTE CT-33-3 ===
def ct33_recomendacao_com_conteudo(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    print("\n📘 Executando CT-33-3 – Abertura Correta do Curso Recomendado com Conteúdo")

    try:
        # 1️⃣ Acessar página inicial
        print(f"🌐 Acessando: {URL}")
        driver.get(URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.save_screenshot("ct33-3_etapa_1_home.png")
        print("🏠 Página Home carregada.")
        time.sleep(3)

        # 2️⃣ Procurar por cursos recomendados
        cursos = driver.find_elements(By.CSS_SELECTOR, "div.MuiGrid-root.MuiGrid-item.css-tolxbf")
        driver.save_screenshot("ct33-3_etapa_2_cursos_recomendados.png")

        if len(cursos) == 0:
            print("❌ Nenhum curso recomendado visível.")
            driver.save_screenshot("ct33-3_etapa_2_erro_nenhum_curso.png")
            return "REPROVADO ❌"

        print(f"✅ Foram encontrados {len(cursos)} cursos recomendados.")

        # 3️⃣ Procurar curso sem PIN e com conteúdo
        curso_com_conteudo = None
        for curso in cursos:
            try:
                curso.find_element(By.CSS_SELECTOR, "svg[data-testid='LockIcon']")
                continue  # tem cadeado, ignora
            except:
                try:
                    # Verifica se há conteúdo visível no card
                    if "vídeo" in curso.text.lower() or "aula" in curso.text.lower() or "conteúdo" in curso.text.lower():
                        curso_com_conteudo = curso
                        break
                except:
                    continue

        if not curso_com_conteudo:
            print("⚠️ Nenhum curso recomendado com conteúdo encontrado.")
            driver.save_screenshot("ct33-3_etapa_3_erro_sem_conteudo.png")
            return "REVISAR ⚠️"

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", curso_com_conteudo)
        driver.execute_script("arguments[0].style.border='3px solid orange';", curso_com_conteudo)
        driver.save_screenshot("ct33-3_etapa_3_curso_com_conteudo.png")
        print("📌 Curso recomendado com conteúdo localizado.")

        # 4️⃣ Clicar no botão "Acessar"
        try:
            botao_acessar = curso_com_conteudo.find_element(
                By.XPATH,
                ".//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'acessar')]"
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", botao_acessar)
            driver.save_screenshot("ct33-3_etapa_4_botao_acessar.png")
            safe_click(driver, botao_acessar)
            print("🖱️ Botão 'Acessar' clicado.")
        except Exception:
            print("❌ Botão 'Acessar' não encontrado.")
            driver.save_screenshot("ct33-3_etapa_4_erro_botao.png")
            return "REPROVADO ❌"

        # 5️⃣ Validar redirecionamento pela mudança de URL
        url_antes = URL
        wait.until(lambda d: d.current_url != url_antes)
        nova_url = driver.current_url
        driver.save_screenshot("ct33-3_etapa_5_url_redirecionada.png")
        print(f"📄 URL após clique: {nova_url}")

        if nova_url != url_antes:
            print("✅ Curso acessado com sucesso.")
            return "APROVADO ✅"
        else:
            print("❌ A URL não mudou após o clique.")
            return "REPROVADO ❌"

    except Exception as e:
        print("⚠️ Erro durante a execução do caso de teste:", e)
        driver.save_screenshot("ct33-3_erro_execucao.png")
        traceback.print_exc()
        return "FALHA ❌"


# === MAIN ===
if __name__ == "__main__":
    driver = setup_driver()
    try:
        resultado = ct33_recomendacao_com_conteudo(driver)
        print(f"\n📊 Resultado do CT-33-3: {resultado}")
        ##driver.save_screenshot("ct33-3_resultado.png")
        print("🖼️ Screenshot salva como ct33-3_resultado.png")
    finally:
        time.sleep(3)
        driver.quit()
        print("🚪 Teste finalizado e navegador fechado.")
