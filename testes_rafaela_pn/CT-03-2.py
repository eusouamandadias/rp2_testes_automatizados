import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys 
from login_selenium import setup_driver, login_usuario, encerrando_driver

def teste_edicao_curso_2(driver):
    print("Iniciando CT3-2: Edição de Curso.")
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://testes.codefolio.com.br/manage-courses")

        print("Passo 1/2: Localizando o curso a ser editado e clicando no botão 'Gerenciar Curso'")
        botao_gerenciar_curso = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='Introdução a IHC']/following::button[text()='Gerenciar Curso'][1]"))
        )
        botao_gerenciar_curso.click()
        time.sleep(3)

        print("Passo 3: Mancando a opção 'Criar PIN para acesso ao curso'")
        botao_ativar_pin = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[1]/div[2]/div[3]/label/span[1]/span[1]"))
        )
        botao_ativar_pin.click()
        time.sleep(3)

        print("Passo 4: Adicionando PIN ao campo 'PIN de Acesso'")
        campo_pin = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[text()='PIN de Acesso']"))
        )
        PIN = driver.find_element(By.ID, campo_pin.get_attribute("for"))
        PIN.send_keys("IHC123")
        time.sleep(3)

        print("Passo 5: Clicando no botão 'Salvar Curso'")
        botao_salvar_curso = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[2]/button[2]"))
        )
        botao_salvar_curso.click()
        time.sleep(3)

        print("Resultado Esperado: A mensagem 'Curso atualizado com sucesso!' deve ser exibida.")
        try:
            mensagem_curso_editado = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Curso atualizado com sucesso!')]"))
            )
            
            assert mensagem_curso_editado.is_displayed()
            print("VERIFICAÇÃO OK: Mensagem 'Curso atualizado com sucesso!' foi exibida.")
            time.sleep(3)

        except TimeoutException:
            print("ERRO: Falha ao exibir a mensagem 'Curso atualizado com sucesso!'")

        botao_ok = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/button"))
        )
        botao_ok.click()
        time.sleep(3)

        driver.get("https://testes.codefolio.com.br/listcurso")
        print("Resultado Esperado: O curso 'Introdução a IHC' deve ser listado na página de cursos agora protegido por PIN.")
        campo_pesquisar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Pesquisar']"))
        )
        campo_pesquisar.click()
        time.sleep(1)
        campo_pesquisar.send_keys("Introdução a IHC")
        time.sleep(3)

        try:
            icone_protegido_por_PIN = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[@data-testid='LockIcon']"))
            )

            assert icone_protegido_por_PIN.is_displayed()
            print("VERIFICAÇÃO OK: Curso 'Introdução a IHC' está protegido por PIN.")
            time.sleep(3)

        except TimeoutException:
            print("ERRO: O curso 'Introdução a IHC' não está protegido por PIN.")

    except Exception as e:
        print("Erro durante a execução do CT3-2: ", e)
        raise

if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_usuario(driver)
        teste_edicao_curso_2(driver)
        
    finally:
        print("Teste finalizado!")
        encerrando_driver(driver)