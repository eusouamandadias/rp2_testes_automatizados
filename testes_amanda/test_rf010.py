"""
Este módulo contém os testes referentes ao Requisito Funcional 010 (RF010) do projeto Codefolio.

Requisito: RF10 – O sistema deve permitir a exclusão de slides de um curso, removendo o material e suas referências.
"""

# Importando bibliotecas necessárias
from playwright.sync_api import sync_playwright, expect

# Importando funções utilitárias
from testes_amanda.utils import load_credentials


# Definindo constantes para o teste RF010
DEFAULT_BROWSER = "chrome"  # Opções: "chrome", "chromium", "firefox", "webkit"
BASE_URL = "https://testes.codefolio.com.br"
COURSE_MANAGEMENT_URL = f"{BASE_URL}/manage-courses"  # Execution Step 01
SLIDE_LESSON_TITLE = "Lição 1 - Preparando o ambiente para testar com Playwright"
MODAL_CONFIRMATION_TEXT = f'Você tem certeza que deseja excluir "{SLIDE_LESSON_TITLE}"?'


def teste_rf010_cancelar_exclusao_slide():
    # Definindo o contexto Playwright
    with sync_playwright() as playwright:
        ############################################################
        #### PRIMEIRA PARTE - INICIALIZAÇÃO E LOGIN ################
        ############################################################
        browser = playwright.chromium.launch(headless=False, channel=DEFAULT_BROWSER)

        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        ###################################################
        ####### SEGUNDA PARTE - ETAPAS DE EXECUÇÃO ########
        ###################################################
        page.goto(COURSE_MANAGEMENT_URL)

        page.locator(".MuiCard-root").filter(
            has_text="Testes Automatizados com Playwright"
        ).get_by_role("button", name="Gerenciar Curso").click()
        page.click('button[role="tab"]:has-text("Slides")')

        page.click('button:has(svg[data-testid="DeleteIcon"])')
        page.get_by_role("button", name="Cancelar").click()

        expect(page.locator(f'text="{SLIDE_LESSON_TITLE}"')).to_have_count(1)


def teste_rf010_slide_excluido_com_sucesso():
    with sync_playwright() as playwright:  # Definindo o contexto Playwright
        ############################################################
        ########## PRIMEIRA PARTE - INICIALIZAÇÃO E LOGIN ##########
        ############################################################
        browser = playwright.chromium.launch(headless=False, channel=DEFAULT_BROWSER)

        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        ###################################################
        #### TEST SOURCE CODE PART 2 - EXECUTION STEPS ####
        ###################################################
        page.goto(COURSE_MANAGEMENT_URL)

        page.click('button:has-text("Gerenciar Curso")')
        page.click('button[role="tab"]:has-text("Slides")')

        page.click('button:has(svg[data-testid="DeleteIcon"])')

        page.click('button:has-text("Excluir")')

        expect(page.locator(f'text="{SLIDE_LESSON_TITLE}"')).to_have_count(0)
