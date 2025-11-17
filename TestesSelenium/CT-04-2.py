import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from login_selenium import setup_driver, login_usuario, encerrando_driver

def teste_exclusao_curso_2(driver):
    print("Iniciando CT4-2: Exclusão de Curso.")
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://testes.codefolio.com.br/manage-courses")
        print("Passo 1/2: Clicando no botão 'Deletar'")
        botao_deletar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div/div/div/div/div[2]/button[2]"))
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

        print("Resultado Esperado: Verificando se a mensagem 'Não é possível deletar o curso pois existem vídeos, materiais, slides ou quizzes associados a ele.' é exibida.")
        try:
            mensagem_exclusao_curso = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Não é possível deletar o curso pois existem vídeos, materiais, slides ou quizzes associados a ele.')]"))
            )
            
            assert mensagem_exclusao_curso.is_displayed()
            print("VERIFICAÇÃO OK: Mensagem 'Não é possível deletar o curso pois existem vídeos, materiais, slides ou quizzes associados a ele.' foi exibida.")
            time.sleep(3)

        except TimeoutException:
            print("ERRO: Falha ao exibir a mensagem 'Não é possível deletar o curso pois existem vídeos, materiais, slides ou quizzes associados a ele.'")

    except Exception as e:
        print("Erro durante a execução do CT4-2: ", e)
        raise

if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_usuario(driver)
        teste_exclusao_curso_2(driver)
        
    finally:
        print("Teste finalizado!")
        encerrando_driver(driver)