from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
from login import setup_driver, login_firebase, TIMEOUT

# Testa acesso a cursos recomendados que não exigem PIN através da home - CT-43

def acessar_curso_recomendado_sem_pin(driver):
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        # Aguardando pelo menos um card de curso recomendado na home
        cards = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MuiCard-root"))
        )

        card_sem_cadeado = None

        # Procurando um card que não tenha o ícone de cadeado
        for card in cards:
            icone_cadeado = card.find_elements(
                By.CSS_SELECTOR,
                ".MuiSvgIcon-root[data-testid='LockIcon']"
            )

            if not icone_cadeado:
                card_sem_cadeado = card
                print("Card sem cadeado encontrado.")
                break

        if not card_sem_cadeado:
            print("Nenhum curso sem PIN foi encontrado na home.")
            return

        time.sleep(2)
        
        # Procurando o botão Acessar dentro do card selecionado
        botao_acessar = card_sem_cadeado.find_element(By.XPATH, ".//button[contains(text(), 'Acessar')]")
        print("Botão Acessar encontrado.")
        
        time.sleep(2)

        # Pega a URL atual antes do clique
        url_antes = driver.current_url
        print(f"URL antes do clique: {url_antes}")
        
        time.sleep(2)
        
        # Clica no botão
        botao_acessar.click()
        print("Clique no botão Acessar realizado.")
        
        time.sleep(2)

        # Aguarda a mudança de URL para confirmar redirecionamento
        try:
            wait.until(lambda d: d.current_url != url_antes)
        except TimeoutException:
            print("A URL não mudou após o clique")
            return

        nova_url = driver.current_url
        print(f"URL após clique: {nova_url}")
        print("Acesso ao curso realizado sem solicitação de PIN.")

    except TimeoutException:
        print("Erro: elemento necessário não foi encontrado dentro do tempo limite.")

    except ElementClickInterceptedException:
        print("Erro: outro elemento interceptou o clique no botão 'Acessar'.")

    except Exception as e:
        print("Erro ao tentar acessar curso recomendado:", e)


# main
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        acessar_curso_recomendado_sem_pin(driver)
    finally:
        time.sleep(2)
        driver.quit()
        print("Teste finalizado e navegador fechado.")
