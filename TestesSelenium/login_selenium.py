import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL = "https://testes.codefolio.com.br/"

FIREBASE_KEY = "firebase:authUser:AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg:[DEFAULT]"

FIREBASE_VALUE = {
    "apiKey": "AIzaSyARn2qVrSSndFu9JSo5mexrQCMxmORZzCg",
    "appName": "[DEFAULT]",
    "createdAt": "1760400653555",
    "displayName": "Rafaela Pacheco Nunes",
    "email": "rafaelanunes.aluno@unipampa.edu.br",
    "emailVerified": True,
    "isAnonymous": False,
    "lastLoginAt": "1761854104973",
    "phoneNumber": None,
    "photoURL": "https://lh3.googleusercontent.com/a/ACg8ocLOyOvwsGmXJ0Mwf_C4tUXUw4D6WCYbZQLoKKrCOAUz0GOTkg=s96-c",
    "providerData": [
        {
            "providerId": "google.com",
            "uid": "106421018055932076561",
            "displayName": "Rafaela Pacheco Nunes",
            "email": "rafaelanunes.aluno@unipampa.edu.br",
            "phoneNumber": None
        }
    ],
    "stsTokenManager": {
        "accessToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjU0NTEzMjA5OWFkNmJmNjEzODJiNmI0Y2RlOWEyZGZlZDhjYjMwZjAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiUmFmYWVsYSBQYWNoZWNvIE51bmVzIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xPeU92d3NHbVhKME13Zl9DNHRVWFV3NEQ2V0NZYlpRTG9LS3JDT0FVejBHT1RrZz1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9yZWFjdC1uYS1wcmF0aWNhIiwiYXVkIjoicmVhY3QtbmEtcHJhdGljYSIsImF1dGhfdGltZSI6MTc2MTg1NDEwNCwidXNlcl9pZCI6Ilc5eUVRNVJveVdnaGVxWTg0UUlMdmw1TVg1VDIiLCJzdWIiOiJXOXlFUTVSb3lXZ2hlcVk4NFFJTHZsNU1YNVQyIiwiaWF0IjoxNzYyNTQ2MTcyLCJleHAiOjE3NjI1NDk3NzIsImVtYWlsIjoicmFmYWVsYW51bmVzLmFsdW5vQHVuaXBhbXBhLmVkdS5iciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTA2NDIxMDE4MDU1OTMyMDc2NTYxIl0sImVtYWlsIjpbInJhZmFlbGFudW5lcy5hbHVub0B1bmlwYW1wYS5lZHUuYnIiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.LFL6nTHu7LBQqr1P0OJ2LuGNKYIhUorlUlD5i6Mc9ByiIGSjbsmmPcpV1Y92ccw4nqCtIAtimfs895XnjzhWTfBfY9dtdNFZ1vY959-RfCeFUlHAlaBdaYLkdXLf-U7unyxArNfUttHjX2xdXZ8rIrVT7Ym10074tu3-_GQeY2gvX5oSVaAmtfMypskf07BQR4aumu96jl0mOrKNUuhZpuoD5DMtzKdi2cFv7kGHXkpqV4cmiiptE8XZTUzl-N2-os3S_WxSu1zQGXeg9j0DSnbGmJbJhJHTmD1cYerhJIFu2mKwAvuSTtAHzj4Iofv9TRI59MNz5XqVZbSKwNIlqQ",
        "expirationTime": 1762549781121,
        "refreshToken": "AMf-vBzvo8A_kK1CK7gGJh7WlKqqViUlwwHc8R6ckomXK9c44Xlyr1_OzDmwRTw-2mH_0uNXReYpQYaE4zusf7BCqow__9GdfrRZmplVWYCxqq95OWXOIW9oEOKwcgLhRSvItI9T0sN_c4xKYHbbgrWGRIwcVAHilQvOkLa1-Mcl5xa_1ceST1Re_NBOT1e78uxUgERr_sE00xjRK2zF6d23No7C1KZKkI-uurHqgSWzJuExvnMsNlzvXU7BXUtg8fCEoLQYTT4wbCa_igRXWQedVqaJcxofvHdVCOyitKa21j_SIIe7d2LJxAE0SbbRJ2Smt_rdz_nFaqlYm7wBUoxcaDHRLMFg6Ugfc2cSp1jOMz8CsgLCwhYiIkF-Yibdw0wz2UB3IhvreyONZQWLdx_S1OrzPIF0FTzhhklCXGcCGzBwEi6J8Mq0yTxghHc6IXIugzm7vpEQEypwuWWA828c9qTuiDJoHQ",
        "tenantId": None
    },
    "uid": "W9yEQ5RoyWgheqY84QILvl5MX5T2",
    "_redirectEventId": None
}

def setup_driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def login_usuario(driver):
    driver.get(URL)
    time.sleep(1)

    print("Injetando dados de autenticação!")
    try:
        driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);",
                FIREBASE_KEY,
                json.dumps(FIREBASE_VALUE))
        print("Token injetado com sucesso!")

    except Exception as e:
        print("Erro ao injetar token: ", e)
        raise

    print("Recarregando a página!")
    driver.refresh()
    time.sleep(5)

    print("Verificando se o login foi processado corretamente!")
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located(
               (By.CSS_SELECTOR, "button[aria-label='Configurações da Conta']")
            )
        )
        print("Login realizado com sucesso!")

    except Exception as e:
        print("Falha ao realizar login! Token pode estar expirado.", e)
        raise

def encerrando_driver(driver):
    print("Fechando navegador!")
    driver.quit()

if __name__ == "__main__":
    driver = setup_driver()
    try:
        login_usuario(driver)
        time.sleep(3)
    finally:
        encerrando_driver(driver)