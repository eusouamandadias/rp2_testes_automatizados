import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutException
from login_selenium import setup_driver, login_usuario, encerrando_driver

def teste_edicao_perfil_2(driver):
    print("Iniciando CT1-2: Edição de Perfil do Usuário.")
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://testes.codefolio.com.br/profile")

        print("Passo 1: Clicando no ícone de edição de perfil")
        botao_edicao_perfil = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[3]/button"))
        )
        botao_edicao_perfil.click()
        time.sleep(5)

        print("Passo 2: Alterando campos de Nome e Sobrenome")
        campo_nome = wait.until(
            EC.visibility_of_element_located((By.NAME, "firstName"))
        )
        campo_nome.send_keys(Keys.CONTROL +"a")
        time.sleep(1)
        campo_nome.send_keys("Rafaela")
        time.sleep(1)

        campo_sobrenome = wait.until(
            EC.visibility_of_element_located((By.NAME, "lastName"))
        )
        campo_sobrenome.send_keys(Keys.CONTROL +"a")
        time.sleep(1)
        campo_sobrenome.send_keys("Nunes")
        time.sleep(1)

        print("Passo 3: Clicando no botão 'SALVAR ALTERAÇÕES'")
        botao_salvar_alteracoes = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/div[2]/form/div/button"))
        )
        botao_salvar_alteracoes.click()
        time.sleep(5)

        print("Resultado Esperado: Verificando mensagem de atualização do perfil.")
        try:
            mensagem_atualizacao = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Perfil atualizado com sucesso!')]"))
            )
            
            assert mensagem_atualizacao.is_displayed()
            print("VERIFICAÇÃO OK: Mensagem 'Perfil atualizado com sucesso!' foi exibida.")
            time.sleep(5)

        except TimeoutException:
            print("ERRO: Falha ao exibir a mensagem 'Perfil atualizado com sucesso!'")

    except Exception as e:
        print("Erro durante a execução do CT1-2: ", e)
        raise

if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_usuario(driver)
        teste_edicao_perfil_2(driver)
        
    finally:
        print("Teste finalizado!")
        encerrando_driver(driver)