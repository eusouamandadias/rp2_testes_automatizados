from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from login import login_firebase, setup_driver, TIMEOUT

#Testa comentários em vídeos do Codefólio - CT-41-1

def comentar_video(driver, comentario="Teste de comentário via Selenium"):
    wait = WebDriverWait(driver, TIMEOUT)

    # Abrir botão comentários
    botao_comentarios = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Comentários']/.."))
    )
    botao_comentarios.click()

    # Digitar comentário na caixa de texto
    campo = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Adicione um comentário...']"))
    )
    campo.send_keys(comentario)

    # Clicar no botão enviar (seta)
    botao_enviar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[not(@disabled)]//*[contains(@data-testid,'SendIcon')]/.."))
    )
    botao_enviar.click()

    # Aguarda um tempo para UI atualizar
    driver.implicitly_wait(2)

    # if que verifica se apareceu mensagem de erro
    erro = driver.find_elements(By.XPATH, "//*[contains(., 'Erro ao postar comentário')]")

    if erro:
        print("O sistema exibiu 'Erro ao postar comentário'.")
        return False

    # if que verifica se comentário foi realmente exibido
    comentario_exibido = driver.find_elements(By.XPATH, f"//*[contains(text(), '{comentario}')]")

    if comentario_exibido:
        print("Comentário enviado e visível na tela.")
        return True
    else:
        print("Nenhum erro exibido, porém o comentário não apareceu.")
        return False

# main
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        comentar_video(driver)
    finally:
        time.sleep(5)
        driver.quit()
        print("Teste finalizado")