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

# login
def login(driver):
    driver.get(URL)
    time.sleep(5)
    json_str = json.dumps(FBASE_VALUE)
    # Usa backticks no JS para preservar qualquer caractere no JSON
    script = f"window.localStorage.setItem({json.dumps(FBASE_KEY)}, `{json_str}`);"
    driver.execute_script(script)
    driver.execute_script("window.location.reload();")
    time.sleep(5)
    print("Login efetuado e página recarregada.")

# Executar caso de teste 17
def testar_consulta_de_alunos(driver):
    wait = WebDriverWait(driver, 5)

    # Clicar na foto de perfil no topo da página.
    print("Clicando no avatar de perfil")
    imagem_perfil = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.MuiAvatar-img")))
    driver.execute_script("arguments[0].click();", imagem_perfil)  # fallback caso o click normal falhe
    time.sleep(5)

    # Selecionar opção “Gerenciamento de Cursos”
    print("Gerenciamento de Cursos...")
    gerenciamento = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Gerenciamento de Cursos')]"))
    )
    driver.execute_script("arguments[0].click();", gerenciamento)
    time.sleep(5)

    # Clicar na opção “Gerenciar Curso”, no curso desejado
    print("Selecionando curso")
    gerenciar_botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Gerenciar Curso')]")))
    gerenciar_botao.click()
    
    time.sleep(5)

    # Selecionar a opção “Alunos”
    print("Abrindo aba de alunos")
    alunos_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alunos')]")))
    
    alunos_tab.click()
    #driver.execute_script("window.scrollTo(//button[contains(., 'Alunos));") #Rolar para o final. execute_script ( "window.scrollTo(0, document.body.scrollHeight);" )
    time.sleep(5)
    
    #Rolar na aba Avaliações
    print("Rolando até a lista de Alunos")
    Alunos_rolar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alunos')]")))
    driver.execute_script("arguments[0].scrollIntoView(true);", Alunos_rolar)
    time.sleep(3)
    
    # Selecionar filtro
    combo = wait.until(EC.element_to_be_clickable(
        (By.ID, "sort-select")
    ))
    combo.click()

    #Filtrando de A-Z
    print("Nomes de A-Z")
    opcao_az = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[@role='option' and @data-value='name-asc']")
    ))
    opcao_az.click()
    
    # Verificar se a lista de alunos é exibida
    print("Lista de Alunos Filtrada de A-Z")
    alunos_linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    aluno_linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    if len(aluno_linhas) > 0:
        print(f"Alunos listados: {len(alunos_linhas)}")
        # Pegando dados da primeira linha
    print("Todas as avaliações:")

    for i, linha in enumerate(aluno_linhas, start=1):
        print(f"{i}. {linha.text}")

# MAIN
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login(driver)
        testar_consulta_de_alunos(driver)
    finally:
        time.sleep(5)
        driver.quit()
        print("Teste finalizado")
