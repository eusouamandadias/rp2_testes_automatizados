from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
from login import setup_driver, login_firebase, TIMEOUT

#Testa curtidas em vídeos do Codefólio - CT-40-1

def clicar_curtir(driver):
    wait = WebDriverWait(driver, TIMEOUT) #wait = instância de espera 
    
    #Procura o botão de curtir
    botao_curtir = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button:has(svg[data-testid="ThumbUpIcon"])'))
        )
        
    botao_curtir.click()
    print("Clique em curtir realizado com sucesso!")
    time.sleep(2) #espera dois segundos pra processar o clique

    # verificação do erro ao curtir
    erro_like = driver.find_elements(
            By.XPATH, "//*[contains(text(), 'Erro ao atualizar like') or contains(text(), 'PERMISSION_DENIED')]"
        )

    if erro_like:
            print("Erro detectado ao curtir: PERMISSION_DENIED.")
    else:
            print("Curtida registrada com sucesso (sem erros visíveis na tela).")

# main
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        clicar_curtir(driver)
    finally:
        time.sleep(2)
        driver.quit()
        print("Teste finalizado e navegador fechado.")