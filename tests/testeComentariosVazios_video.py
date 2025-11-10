from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from login import login_firebase, setup_driver, TIMEOUT

#Testa comentários vazios (em branco) em vídeos do Codefólio - CT-41-2

def testar_comentario_vazio(driver):
    wait = WebDriverWait(driver, TIMEOUT)

    # Abrir botão comentários
    botao_comentarios = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Comentários']/.."))
    )
    botao_comentarios.click()

    # Localizar campo de comentário
    campo = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Adicione um comentário...']"))
    )
    # Deixar o campo vazio (ou seja, sem texto algum)
    campo.clear()

    # Verificar se o botão de envio está desabilitado
    try:
        botao_enviar = driver.find_element(By.XPATH, "//button[@disabled]//*[contains(@data-testid,'SendIcon')]/..")
        print("O sistema impediu o envio de comentário vazio.")
        return True
    except:
        print("O botão de envio está habilitado mesmo com o campo vazio.")
        return False

# main
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        testar_comentario_vazio(driver)
    finally:
        time.sleep(5)
        driver.quit()
        print("Teste finalizado")
