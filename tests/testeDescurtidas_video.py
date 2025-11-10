from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
from login import setup_driver, login_firebase, TIMEOUT

#Testa descurtidas em vídeos do Codefólio - CT-40-2

def clicar_descurtir(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    
    botao_descurtir = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button:has(svg[data-testid="ThumbDownIcon"])'))
        )
        # Clica no botão
    botao_descurtir.click()
    print("Clique em descurtir realizado com sucesso!")
    time.sleep(2)

    # verificação do erro ao descurtir
    erro_dislike = driver.find_elements(
            By.XPATH,
            "//*[contains(text(), 'Erro ao atualizar dislike') or contains(text(), 'PERMISSION_DENIED')]"
        )

    if erro_dislike:
            print("Erro detectado ao descurtir: PERMISSION_DENIED.")
    else:
            print("Descurtida registrada com sucesso (sem erros visíveis na tela).")

# main
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        clicar_descurtir(driver)
    finally:
        time.sleep(2)
        driver.quit()
        print("Teste finalizado e navegador fechado.")