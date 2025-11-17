import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys 
from login_selenium import setup_driver, login_usuario, encerrando_driver

def teste_cadastro_curso(driver):
    print("Iniciando CT2: Cadastro de Curso.")
    wait = WebDriverWait(driver, 10)

    try:
        print("Passo 1: Clicando no menu da página")
        botao_menu = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section[2]/div[2]/div/div[1]/div/div[2]/button[2]"))
        )
        botao_menu.click()
        time.sleep(3)
        
        print("Passo 2: Clicando no item 'Gerenciamento de Cursos' do menu")
        botao_gerenciamento_cursos = wait.until(
            EC.presence_of_element_located((By.XPATH, "//li[contains(., 'Gerenciamento de Cursos')]"))
        )
        botao_gerenciamento_cursos.click()
        time.sleep(3)

        print("Passo 3: Clicando no botão 'Criar Novo Curso'")
        botao_criar_curso = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/button"))
        )
        botao_criar_curso.click()
        time.sleep(3)

        print("Passo 4: Preenchendo os campos 'Título do Curso' e 'Descrição'")
        campo_titulo_curso = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[text()='Título do Curso']"))
        )
        titulo_curso = driver.find_element(By.ID, campo_titulo_curso.get_attribute("for"))
        titulo_curso.send_keys("Introdução a IHC")
        time.sleep(3)

        campo_descricao_curso = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//label[text()='Descrição do Curso']"))
        )
        descricao_curso = driver.find_element(By.ID, campo_descricao_curso.get_attribute("for"))
        descricao_curso.send_keys("Curso básico sobre Interação Humano-Computador")
        time.sleep(3)

        print("Passo 6: Clicando no botão 'SALVAR CURSO'")
        botao_salvar_curso = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[2]/button[2]"))
        )
        botao_salvar_curso.click()
        time.sleep(3)

        print("Resultado Esperado: Verificando mensagem de criação do curso.")
        try:
            mensagem_curso_criado = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Curso criado com sucesso!')]"))
            )
            
            assert mensagem_curso_criado.is_displayed()
            print("VERIFICAÇÃO OK: Mensagem 'Curso criado com sucesso!' foi exibida.")
            time.sleep(3)


        except TimeoutException:
            print("ERRO: Falha ao exibir a mensagem 'Curso criado com sucesso!'")

        print("Passo 7: Clicando no botão 'OK' após a exibição da mensagem")
        botao_OK = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/button"))
        )
        botao_OK.click()
        time.sleep(1)

        botao_cancelar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[2]/button[1]"))
        )
        botao_cancelar.click()
        time.sleep(1)
            
        print("Passos 8 e 9: Curso deve estar listado na página /listcurso.")
        driver.get("https://testes.codefolio.com.br/listcurso")
        campo_pesquisar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Pesquisar']"))
        )
        campo_pesquisar.click()
        time.sleep(1)
        campo_pesquisar.send_keys("Introdução a IHC")
        time.sleep(3)
        try:
            curso_encontrado = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Introdução a IHC')]"))
            )
            
            assert curso_encontrado.is_displayed()
            print("VERIFICAÇÃO OK: Curso 'Introdução a IHC' foi encontrado na lista de cursos.")
            time.sleep(3)

        except TimeoutException:
            print("ERRO: Falha ao tentar encontrar o curso 'Introdução a IHC' na liata de cursos.")

    except Exception as e:
        print("Erro durante a execução do CT2: ", e)
        raise

if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_usuario(driver)
        teste_cadastro_curso(driver)
        
    finally:
        print("Teste finalizado!")
        encerrando_driver(driver)