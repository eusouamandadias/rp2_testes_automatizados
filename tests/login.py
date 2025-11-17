import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

#arquivo para separar o login e configuração do ambiente de teste

URL = "https://testes.codefolio.com.br/"
TIMEOUT = 10

#Dados de login
FBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"
FBASE_VALUE = {
        "apiKey": "AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg",
        "appName": "[DEFAULT]",
        "createdAt": "1760400642600",
        "displayName": "Tauani Ximenes Sauceda",
        "email": "tauanisauceda.aluno@unipampa.edu.br",
        "emailVerified": True,
        "isAnonymous": False,
        "lastLoginAt": "1762649803939",
        "phoneNumber": None,
        "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocK62SxP9tM72P6a9yed15BnoXLtH-AUAlAKOfrvQW7r3t-mRA=s96-c",
        "providerData": [
            {
                "providerId": "google.com",
                "uid": "106027413228480034197",
                "displayName": "Tauani Ximenes Sauceda",
                "email": "tauanisauceda.aluno@unipampa.edu.br",
                "phoneNumber": None,
                "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocK62SxP9tM72P6a9yed15BnoXLtH-AUAlAKOfrvQW7r3t-mRA=s96-c"
            }
        ],
        "stsTokenManager": {
            "accessToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NTEzMjA5OWFkNmJmNjEzODJiNmI0Y2RlOWEyZGZlZDhjYjMwZjAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiVGF1YW5pIFhpbWVuZXMgU2F1Y2VkYSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLNjJTeFA5dE03MlA2YTl5ZWQxNUJub1hMdEgtQVVBbEFLT2ZydlFXN3IzdC1tUkE9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vcmVhY3QtbmEtcHJhdGljYSIsImF1ZCI6InJlYWN0LW5hLXByYXRpY2EiLCJhdXRoX3RpbWUiOjE3NjI2NDk4MDMsInVzZXJfaWQiOiJ5dmVaelVNbnMyWlhDcEcza2h5bkZhVWxkZEgzIiwic3ViIjoieXZlWnpVTW5zMlpYQ3BHM2toeW5GYVVsZGRIMyIsImlhdCI6MTc2MjY0OTgwMywiZXhwIjoxNzYyNjUzNDAzLCJlbWFpbCI6InRhdWFuaXNhdWNlZGEuYWx1bm9AdW5pcGFtcGEuZWR1LmJyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDYwMjc0MTMyMjg0ODAwMzQxOTciXSwiZW1haWwiOlsidGF1YW5pc2F1Y2VkYS5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.FLJ_Z35yoenorSmspsEGuW4qzVycHvwPj5rLvbzORM1WStpH4J-Lg_V5V1VXU4r5Y1Y5KmR-MxKLo9ekHwjkJiojhtpvTG42-KP8G6LDdOwi1lqQH2i7SVzGQYaXIpqrmzKV6pbHnnU5soTtOKmEIvwuuzGMFvHD_7Eyz6A0SgLVqfKQ3b3dzIPz5mkd4KAJR3CH4WGpZX8WgYrFx-XAdtmtGVSE3ygYroo7f9rp1WOkEBWkEdTQKadRZXPfVMO4QI53bPhRw3xJDyGyi85D-qijvvHbtkQyFbHJSXTWfiXH3SPHMFTvXM2uPbV_E7kZBUcvjH3nowH-vEdxbdCYUw",
            "expirationTime": 1762653404479,
            "refreshToken": "AMf-vBxszTtzfHMbbMV-nZp_3ZcfJRi-hevvMsJOY0S9lP11Tsdch9hUlJEtDFJBQhjrgfbTGrz63x1w--avN1noyzVoPjetzHO1nNiWo2GI8gNpCPUhDoMBeqXRC8Y44ke1XZhd4jjrW4ExrXFJgfgl5me2UTWqI6dJhRb0EJu1XNI2CDVf4vzV_1ZPZyL5OBPtPSsKNieUYKH-aw_I26VOfT0npbmonseWcFLf9BwVZ-mGdBTT_fbewhwSnrDnOtsTOCaoGSisxlGDMfBrUDPgknHm_HImMn9-Zom6Ffkklsh_i2rxJiP004WsFUe7OmDtqxnq1sGZJqJ7L-3HF00l_og2nJ81G5qqWLwrk-wFOhyC8u8F5FAyAcr9tv2bbOpAZuReyjnCMlzlVkkKhoQigex4gzf6cBYm9sOJREjBrpEigvtNMROiKTTj1Vrcv-IS74poKQIGTrgW_KPv0p7is_BH6D0c-Q"
        },
        "tenantId": None,
        "uid": "yveZzUMns2ZXCpG3khynFaUlddH3",
        "_redirectEventId": None
    }

#configuração do webdriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

#injetar login
def login_firebase(driver):
    driver.get(URL)
    time.sleep(1)
    json_str = json.dumps(FBASE_VALUE)
    script = f"window.localStorage.setItem({json.dumps(FBASE_KEY)}, `{json_str}`);"
    driver.execute_script(script)
    driver.execute_script("window.location.reload();")
    time.sleep(4)
    print("Login injetado e página recarregada.")

#executando testes
def testar_funcionalidades(driver):
    wait = WebDriverWait(driver, 10)

    print("Verificando se está logado...")
    try:
        profile_img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img, .profile, .user-avatar")))
        print("Login detectado com sucesso!")
    except:
        print("Perfil não encontrado.")

# main
if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_firebase(driver)
        testar_funcionalidades(driver)
    finally:
        time.sleep(2)
        driver.quit()
        print("Teste finalizado e navegador fechado.")