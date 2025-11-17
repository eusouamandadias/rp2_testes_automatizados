import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys 
from login_selenium import setup_driver, login_usuario, encerrando_driver

def teste_edicao_curso_1(driver):
    print("Iniciando CT3-1: Edição de Curso.")
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://testes.codefolio.com.br/manage-courses")

        print("Passo 1/2: Localizando o curso a ser editado e clicando no botão 'Gerenciar Curso'")
        botao_gerenciar_curso = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div/div/div/div/div[2]/button[1]"))
        )
        botao_gerenciar_curso.click()
        time.sleep(3)

        print("Passo 3: Alterando o campo 'Título do Curso'")
        try:
            edicao_campo_titulo = wait.until(
                EC.presence_of_element_located((By.XPATH, "//label[text()='Título do Curso']"))
            )
            titulo_curso = driver.find_element(By.ID, edicao_campo_titulo.get_attribute("for"))
            #titulo_curso.send_keys(Keys.CONTROL +"a")
            #time.sleep(1)
            titulo_curso.send_keys("IHC - Fundamentos")
            time.sleep(3)

        except (TimeoutException, NoSuchElementException) as e:
            print("ERRO: Não foi possível encontrar ou interagir com o campo 'Título do Curso'. ", e)

        print("Passo 4: Alterando o campo 'Descrição do Curso'")
        try:
            edicao_campo_descricao = wait.until(
                EC.presence_of_element_located((By.XPATH, "//label[text()='Descrição do Curso']"))
            )
            descricao_curso = driver.find_element(By.ID, edicao_campo_descricao.get_attribute("for"))
            #descricao_curso.send_keys(Keys.CONTROL +"a")
            #time.sleep(1)
            descricao_curso.send_keys("Introdução à Interação Humano-Computador")
            time.sleep(3)

        except (TimeoutException, NoSuchElementException) as e:
            print("ERRO: Não foi possível encontrar ou interagir com o campo 'Descrição do Curso'. ", e)

    except Exception as e:
        print("Erro durante a execução do CT3-1: ", e)
        raise

if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_usuario(driver)
        teste_edicao_curso_1(driver)
        
    finally:
        print("Teste finalizado!")
        encerrando_driver(driver)