from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
from login import setup_driver, login_firebase, TIMEOUT

# Testa compartilhamento indireto de vídeos acessados na home através do link copiado - CT-42

def compartilhar_video_link(driver):
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        # Aguarda a presença de um vídeo na home
        video = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiCard-root"))
        )
        print("Vídeo localizado na home!")

        # Procura o botão de compartilhar do sistema

        botao_compartilhar = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[data-testid="ShareIcon"]'))
        )
        print("Botão de compartilhar encontrado!")
        time.sleep(2)

        # Clica no botão de compartilhar
        botao_compartilhar.click()
        print("Clique no botão de compartilhar realizado!")
        time.sleep(2)

        # Verifica se a plataforma indica que o link foi copiado
        mensagem_sucesso = driver.find_elements(
            By.XPATH,
            "//*[contains(text(), 'copiado') or contains(text(), 'Copiado') or contains(text(), 'transferência')]"
        )

        if mensagem_sucesso:
            print("URL copiada para a área de transferência com sucesso!")
        else:
            print("Nenhuma mensagem de confirmação foi exibida. Pode ser necessária verificação manual.")

    except TimeoutException:
        print("Erro: elemento necessário não foi encontrado dentro do tempo limite.")

    except ElementClickInterceptedException:
        print("Erro: outro elemento interceptou o clique no botão de compartilhar.")

    except Exception as e:
        print("Erro ao tentar compartilhar vídeo:", e)

# main
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        compartilhar_video_link(driver)
    finally:
        time.sleep(2)
        driver.quit()
        print("Teste finalizado e navegador fechado.")
