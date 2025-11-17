import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from login_selenium import setup_driver, login_usuario, encerrando_driver

def teste_exclusao_curso_1(driver):
    print("Iniciando CT4-1: Exclusão de Curso.")
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://testes.codefolio.com.br/manage-courses")
        print("Passo 1/2: Clicando no botão 'Deletar'")
        botao_deletar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Introdução a IHC']/following::button[text()='Deletar'][1]"))
        )
        botao_deletar.click()
        time.sleep(3)

        print("Passo 3: Verificando mensagem de confirmação de exclusão do curso.")
        try:
            mensagem_exclusao_curso = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Tem certeza que deseja deletar esse curso?')]"))
            )
            
            assert mensagem_exclusao_curso.is_displayed()
            print("VERIFICAÇÃO OK: Mensagem 'Tem certeza que deseja deletar esse curso?' foi exibida.")
            time.sleep(3)

        except TimeoutException:
            print("ERRO: Falha ao exibir a mensagem 'Tem certeza que deseja deletar esse curso?'")

        print("Passo 4: Clicando novamente em 'Deletar'")
        deletar_curso = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div/button[2]"))
        )
        deletar_curso.click()
        time.sleep(3)

        print("Resultado Esperado: Verificando mensagem de exclusão do curso.")
        try:
            mensagem_exclusao_curso = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Curso deletado com sucesso')]"))
            )
            
            assert mensagem_exclusao_curso.is_displayed()
            print("VERIFICAÇÃO OK: Mensagem 'Curso deletado com sucesso!' foi exibida.")
            time.sleep(3)

        except TimeoutException:
            print("ERRO: Falha ao exibir a mensagem 'Curso deletado com sucesso!'")

        print("Resultado Esperado: O curso deletado não deve estar mais listado nas páginas /manage-courses e /listcurso.")
        try:
            driver.get("https://testes.codefolio.com.br/manage-courses")

            curso_nao_encontrado = wait.until(
                EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Introdução a IHC')]"))
            )
            
            print("VERIFICAÇÃO OK: O curso 'Introdução a IHC' não foi encontrado na página /manage-courses, como esperado.")

        except TimeoutException:
            print("ERRO: O curso 'Introdução a IHC' foi encontrado na página /manage-courses, mas não deveria.")

        try:
            driver.get("https://testes.codefolio.com.br/listcurso")
            campo_pesquisar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Pesquisar']"))
            )
            campo_pesquisar.click()
            time.sleep(1)
            campo_pesquisar.send_keys("Introdução a IHC")
            time.sleep(3)

            curso_nao_encontrado = wait.until(
                EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Introdução a IHC')]"))
            )
            
            print("VERIFICAÇÃO OK: O curso 'Introdução a IHC' não foi encontrado na página /listcurso, como esperado.")

        except TimeoutException:
            print("ERRO: O curso 'Introdução a IHC' foi encontrado na página /listcurso, mas não deveria.")

    except Exception as e:
        print("Erro durante a execução do CT4-1: ", e)
        raise

if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_usuario(driver)
        teste_exclusao_curso_1(driver)
        
    finally:
        print("Teste finalizado!")
        encerrando_driver(driver)