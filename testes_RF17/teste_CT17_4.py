import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://testes.codefolio.com.br/"

# Chave do localStorage
FBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"

# Minha value 
FBASE_VALUE = {
  "apiKey": "AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg",
  "appName": "[DEFAULT]",
  "createdAt": "1760400650585",
  "displayName": "Izabel de Oliveira Boaventura",
  "email": "izabelboaventura.aluno@unipampa.edu.br",
  "emailVerified": True,
  "isAnonymous": False,
  "lastLoginAt": "1762626262963",
  "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocJI6RV84xezcRbUUKCZYIPnBQjwcWKXGRYosRZ37Kx7hi0cRw=s96-c",
  "providerData": [
    {
      "providerId": "google.com",
      "uid": "104672506054660683732",
      "displayName": "Izabel de Oliveira Boaventura",
      "email": "izabelboaventura.aluno@unipampa.edu.br",
      "phoneNumber": None,
      "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocJI6RV84xezcRbUUKCZYIPnBQjwcWKXGRYosRZ37Kx7hi0cRw=s96-c"
    }
  ],
  "stsTokenManager": {
    # AccessToken completo
    "accessToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NTEzMjA5OWFkNmJmNjEzODJiNmI0Y2RlOWEyZGZlZDhjYjMwZjAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiSXphYmVsIGRlIE9saXZlaXJhIEJvYXZlbnR1cmEiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSkk2UlY4NHhlemNSYlVVS0NaWUlQbkJRandjV0tYR1JZb3NSWjM3S3g3aGkwY1J3PXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3JlYWN0LW5hLXByYXRpY2EiLCJhdWQiOiJyZWFjdC1uYS1wcmF0aWNhIiwiYXV0aF90aW1lIjoxNzYyNjI2MjYyLCJ1c2VyX2lkIjoiZDVxbllIM2UyWll5bE5tVFY4UVA0d2dlNlQ2MiIsInN1YiI6ImQ1cW5ZSDNlMlpZeWxObVRWOFFQNHdnZTZUNjIiLCJpYXQiOjE3NjI2MjYyNjIsImV4cCI6MTc2MjYyOTg2MiwiZW1haWwiOiJpemFiZWxib2F2ZW50dXJhLmFsdW5vQHVuaXBhbXBhLmVkdS5iciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTA0NjcyNTA2MDU0NjYwNjgzNzMyIl0sImVtYWlsIjpbIml6YWJlbGJvYXZlbnR1cmEuYWx1bm9AdW5pcGFtcGEuZWR1LmJyIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.NSB0UEbf9DTxkVBu42fuOGygaeYl81YA1ng6d6gm_ZbIFmTUVnob3OX6QQxLN8WfrR4t4zCVT82m1vbcOGac7ZqmvhXBVRVgfefi4UuG29k5RIKwUwXqT8ALqqVKMQ3g3vxk41MRbja3EqWpWNXLfgwKWkHSqlE13NtCJ9xktyR4FMub3R0V7qCcU5WL_YSvh1-OsVoPej9K3rqD9294Io7Roeg3tL4Po2vL3_NaVHg3hD5pxtk8K4viZl_w4H3PfGMe5rnfR1MGsymsT_iertpgkkehmhnMaYUKCNBEIvdpJzCZnzoSQKGbkkg08rIusMKfgFRCOJcaBVG5xOPsVA",
    # expirationTime: número
    "expirationTime": 1762629863996,
    # refreshToken que veio no JSON do DevTools
    "refreshToken": "AMf-vBwC2Q_JAEWoL5QGMCuSTGG7E49nPK2JSZuTN6f5CpgX-ika4HAulVxATMGaH9EdwOFBwDbFZfbNVN10zoh44YDLPpzYJKKPOC1pRrDxToAYZn_DrVs96LgUM6SqGPu-Czq7EPPisOSpdCWm_mlPg_eN31CsLm7nWX5y1BihgJHqTgfxcIIzXY8YFyb3QdsmmbLofLZwq_JXgPAxGtzVt6iaw_iuTwAstXcV5EtSpXaWa6GypiLaE0voI9P8Lq7MO7jUqYt8vF04wLBoFZhsajMVENaA1NG2pCM8URBPX4b2hnHrlrmNiW5SdZ4BEKSkrmSlO3Jg7Vr2z1dPb58mmSbwkyiRJSXNp4euuGlnoE053_-5Zj3ZphD9YzL94BaLau9_4XGMq0rIRkHP7nauQvccfsevB1fn3fWWU-pGkye1vPs5ErkShFVFiaAKJ4V3FlTdlxVGfSP9tVdMIVIgV45HKCovoxbPcPDhjrbefD0Vk74MbWg"
  },
  "uid": "d5qnYH3e2ZYylNmTV8QP4wge6T62"
}

# Configuração Selenium
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Sessão Firebase
def login_firebase(driver):
    driver.get(URL)
    time.sleep(1)
    json_str = json.dumps(FBASE_VALUE)
    # Usa backticks no JS para preservar qualquer caractere no JSON
    script = f"window.localStorage.setItem({json.dumps(FBASE_KEY)}, `{json_str}`);"
    driver.execute_script(script)
    driver.execute_script("window.location.reload();")
    time.sleep(4)
    print("Login efetuado e página recarregada.")

# Executar Caso de Teste 17-2
def testar_consulta_de_alunos_se_o_Aluno_Ainda_Aparece_na_Lista_Apos_sua_Remoção(driver):
    wait = WebDriverWait(driver, 15)

    # Clicar na foto de perfil
    print("Clicando no avatar de perfil")
    imagem_perfil = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.MuiAvatar-img")))
    driver.execute_script("arguments[0].click();", imagem_perfil)
    time.sleep(1)

    # Selecionar “Gerenciamento de Cursos”
    print("Abrindo Gerenciamento de Cursos...")
    gerenciamento = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Gerenciamento de Cursos')]"))
    )
    driver.execute_script("arguments[0].click();", gerenciamento)
    time.sleep(1)

    # Selecionar o curso
    print("Selecionando curso 'Teste Avaliação'")
    curso = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class,'MuiCard-root')][.//h6[normalize-space(text())='Teste Avaliação']]")
    ))

    botao_gerenciar = curso.find_element(By.XPATH, ".//button[contains(., 'Gerenciar Curso')]")
    driver.execute_script("arguments[0].click();", botao_gerenciar)
    time.sleep(2)

    # Abrir aba "Alunos"
    print("Abrindo aba de alunos...")
    alunos = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alunos')]")))
    alunos.click()
    time.sleep(3)
    
    #Rolar ate a aba alunos
    print("Rolando ate a lista de alunos")
    alunos_rolar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alunos')]")))
    driver.execute_script("arguments[0].scrollIntoView(true);", alunos_rolar)
    time.sleep(3)


    # Selecionar primeira linha (primeiro aluno da lista)
    primeira_linha = wait.until(EC.presence_of_element_located(
        (By.XPATH, "(//table//tr)[2]") # TR[1] é cabeçalho
    ))

    # Captura o nome do aluno que será removido (para validar)
    aluno_nome = primeira_linha.find_element(By.XPATH, ".//td[1]").text
    print(f"Aluno encontrado para remoção: {aluno_nome}")

    # Botão de excluir dentro dessa linha
    botao_excluir = primeira_linha.find_element(By.XPATH, ".//button[.//*[@data-testid='DeleteIcon']]")
    driver.execute_script("arguments[0].click();", botao_excluir)
    time.sleep(3)

    # Confirmar exclusão
    botao_confirmar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Confirmar']"))
    )
    driver.execute_script("arguments[0].click();", botao_confirmar)
    time.sleep(3)

    # Verificar se aluno sumiu da lista
    recaregar_pagina = driver.page_source

    if aluno_nome not in recaregar_pagina:
        print("O aluno foi removido da lista.")
    else:
        print("O aluno ainda aparece na lista após remoção.")
    
    

# MAIN
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        testar_consulta_de_alunos_se_o_Aluno_Ainda_Aparece_na_Lista_Apos_sua_Remoção(driver)
    finally:
        time.sleep(6)
        driver.quit()
        print("Teste finalizado")
