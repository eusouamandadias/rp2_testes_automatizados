from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
from login import setup_driver, login_firebase, TIMEOUT

#Testa acesso a cursos recomendados que exigem PIN através da home - CT-44-1

def acessar_curso_recomendado_com_pin(driver):
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        # Aguardar carregamento dos cards de cursos recomendados
        cards = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MuiCard-root"))
        )

        card_com_cadeado = None

        # Encontrar card com ícone de cadeado (curso com PIN)
        for card in cards:
            icone_cadeado = card.find_elements(
                By.CSS_SELECTOR,
                ".MuiSvgIcon-root[data-testid='LockIcon']"
            )

            if icone_cadeado:
                card_com_cadeado = card
                print("Card com PIN encontrado.")
                break

        if not card_com_cadeado:
            print("Nenhum curso com PIN foi encontrado na home.")
            return

        time.sleep(2)

        # Procurando o botão Acessar dentro do card selecionado
        botao_acessar = card_com_cadeado.find_element(By.XPATH, ".//button[contains(text(), 'Acessar')]")
        print("Botão Acessar encontrado.")

        url_antes = driver.current_url
        botao_acessar.click()
        print("Clique no botão Acessar realizado.")

        # Esperar pedido de pin
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'PIN de acesso') or contains(text(), 'PIN de Acesso')]")
            )
        )
        print("Modal de PIN detectado.")

        # Campo do PIN
        pin = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//div[contains(@class, 'MuiOutlinedInput-root') and contains(., 'PIN')]")
            )
        )
        pin_input = pin.find_element(By.XPATH, ".//input")

        # Inserindo o PIN no campo de entrada
        pin_teste = "123" 
        pin_input.send_keys(pin_teste)
        print("PIN inserido.")

        # Clique no botão enviar, após inserir o PIN
        botao_enviar = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Enviar')]")
            )
        )
        botao_enviar.click()
        print("Botão Enviar clicado.")

        # Verificar redirecionamento
        try:
            wait.until(lambda d: d.current_url != url_antes)
            print("Redirecionamento realizado. Acesso ao curso com PIN.")
        except TimeoutException:
            print("A URL não mudou após clicar em Enviar.")
            return

    except Exception as e:
        print("Erro durante o teste:", e)


if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        acessar_curso_recomendado_com_pin(driver)
    finally:
        time.sleep(2)
        driver.quit()
        print("Teste finalizado e navegador fechado.")
