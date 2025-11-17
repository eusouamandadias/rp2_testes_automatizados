"""
Este módulo contém os testes referentes ao Requisito Funcional 009 (RF009) do projeto Codefolio.

Requisito: RF9 – O sistema deve permitir editar informações ou substituir slides já cadastrados.
"""

# Importando bibliotecas necessárias
from re import A, T
from time import time
from playwright.sync_api import sync_playwright, expect

# Importando funções utilitárias
from tests.utils import load_credentials


# Definindo constantes para o teste RF009
DEFAULT_BROWSER = "chrome"  # Opções: "chrome", "chromium", "firefox", "webkit"
BASE_URL = "https://testes.codefolio.com.br"
COURSE_MANAGEMENT_URL = f"{BASE_URL}/manage-courses"
NEW_SLIDE_TITLE = "Lição 1 - Preparando o ambiente para testar com Playwright"
NEW_HTML_CODE = "https://docs.google.com/presentation/d/e/2PACX-1vSzcPobWyEazwXnAFux9eVqLFBMeC3yQuKbRvpgRO2OsAv34A4BJWfAXLfsDPl2vNYeUATNdVwnI4LI/pubembed?start=false&loop=false&delayms=30000"
MESSAGE_TEXT = "O slide foi atualizado com sucesso!"
TEMPO_DE_PAUSA = 3000

# Antes de começar co o test rf009, precisamos verificar se o slide "Introdução ao Playwright" já existe e se não, criá-lo.
def test_criando_novo_slide():
    # Criar um contexto Playwright
    with sync_playwright() as playwright:
        # Inicializando o navegador
        browser = playwright.chromium.launch(headless=False, channel=DEFAULT_BROWSER)

        # Carregando credenciais de login armazenadas e criando uma nova página
        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        page.wait_for_timeout(TEMPO_DE_PAUSA)
        # Accessar a página de gerenciamento de conteúdo do curso
        print("\n\nIndo para a página de gerenciamento de cursos...\n")
        page.goto(COURSE_MANAGEMENT_URL)
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        card_do_curso = page.locator(".MuiCard-root").filter(
            has_text="Testes Automatizados com Playwright"
        )
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        botao_gerenciar = card_do_curso.get_by_role("button", name="Gerenciar Curso")
        print(
            f"Clicando em 'Gerenciar Curso' para o curso: {'Testes Automatizados com Playwright'}"
        )
        page.wait_for_timeout(TEMPO_DE_PAUSA)
        botao_gerenciar.click()

        page.click('button[role="tab"]:has-text("Slides")')

        page.wait_for_timeout(TEMPO_DE_PAUSA)
        slide_card = page.locator("div.MuiPaper-root.MuiPaper-elevation2").filter(
            has_text="Introdução ao Playwright"
        )
        if slide_card.count() == 0:
            # Preenchendo o formulário para adicionar um novo slide
            titulo_input_id = page.get_by_label("Título do Slide")
            titulo_input_id.fill("Introdução ao Playwright")
            page.wait_for_timeout(TEMPO_DE_PAUSA)

            url_input_id = page.get_by_label("URL do Slide (Google Apresentações)")
            url_input_id.fill(NEW_HTML_CODE)
            page.wait_for_timeout(TEMPO_DE_PAUSA)

            page.click('button:has-text("Adicionar Slide")')
            page.wait_for_timeout(5000)

        # expect(
        #     page.locator("div.MuiPaper-root.MuiPaper-elevation2").filter(
        #         has_text="Introdução ao Playwright"
        #     )
        # ).to_have_count(1)


def test_rf009_edit_slide_success():
    # Criando um contexto Playwright
    with sync_playwright() as playwright:
        ############################################################
        ########## PRIMEIRA PARTE - INICIALIZAÇÃO E LOGIN ##########
        ############################################################
        # Inicializando o navegador
        browser = playwright.chromium.launch(headless=False, channel=DEFAULT_BROWSER)

        # Carregando credenciais de login armazenadas e criando uma nova página
        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        ###################################################
        ####### SEGUNDA PARTE - ETAPAS DE EXECUÇÃO ########
        ###################################################
        # Acessando a página de gerenciamento de conteúdo do curso
        page.goto(COURSE_MANAGEMENT_URL)

        # Clicando no primeiro botão com o texto "Gerenciar Curso" na página
        page.click('button:has-text("Gerenciar Curso")')

        # Acessar a aba "Slides"
        page.click('button[role="tab"]:has-text("Slides")')
        # Clicando no ícone "Editar" do slide "Introdução ao Playwright".
        # Encontramos esse botão pois é o primeiro na página com um svg dentro dele.
        page.click('button:has(svg[data-testid="EditIcon"])')

        # Alterando o campo "Título do Slide" para "NEW_SLIDE_TITLE".
        # Encontramos esse input limpando primeiro e depois preenchendo o campo de título do slide
        slide_title_id = "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation2 div.MuiInputBase-root input"
        slide_title_input = page.locator(slide_title_id).first
        slide_title_input.clear()
        slide_title_input.fill(NEW_SLIDE_TITLE)

        # Substituir o conteúdo do campo "Código HTML" por um novo código de incorporação válido
        # Encontramos esse input pois ele está dentro do segundo div com a classe "MuiInputBase-root"
        slide_url_id = "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation2 div.MuiInputBase-root input"
        slide_url_input = page.locator(slide_url_id).nth(1)
        slide_url_input.clear()
        slide_url_input.fill(NEW_HTML_CODE)

        # Clicar em "Salvar Alterações"
        # Encontramos esse botão pois é o único com o texto "Salvar Alterações"
        page.click('button:has-text("Salvar Alterações")')

        # Verificando se a mensagem de sucesso é exibida
        page.locator("#success-dialog-description").wait_for(
            state="visible", timeout=10000
        )

        success_dialog = page.locator("#success-dialog-description")
        expect(success_dialog).to_be_visible()
        page.get_by_role("button", name="OK").click()
        success_dialog.wait_for(state="hidden", timeout=10000)

        page.wait_for_selector(f'h6:has-text("{NEW_SLIDE_TITLE}")', timeout=10000)
        slide_title = page.locator(f'h6:has-text("{NEW_SLIDE_TITLE}")')
        expect(slide_title).to_be_visible()


def test_rf009_edit_slide_failed_with_empty_title():
    # Criando um contexto Playwright
    with sync_playwright() as playwright:
        ############################################################
        ########## PRIMEIRA PARTE - INICIALIZAÇÃO E LOGIN ##########
        ############################################################
        # Inicializando o navegador
        browser = playwright.chromium.launch(headless=False, channel=DEFAULT_BROWSER)

        # Carregando credenciais de login armazenadas e criando uma nova página
        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        ###################################################
        ####### SEGUNDA PARTE - ETAPAS DE EXECUÇÃO ########
        ###################################################
        # Acessar a página de gerenciamento de conteúdo do curso
        page.goto(COURSE_MANAGEMENT_URL)

        # Acessar uma página de gerenciamento de curso que contém lições de slides
        # Para fazer isso, clicamos no primeiro botão com o texto "Gerenciar Curso" na página
        page.click('button:has-text("Gerenciar Curso")')

        # Acessar a aba "Slides"
        page.click('button[role="tab"]:has-text("Slides")')

        # Acessar o ícone "Editar" para os slides "Exemplo 01".
        # Encontramos esse botão pois é o primeiro botão na página com um svg dentro dele.
        page.click('button:has(svg[data-testid="EditIcon"])')

        # Alterar o campo "Título do Slide" para "".
        # Encontramos esse input pois primeiro limpamos e depois preenchemos o campo de título do slide
        slide_title_id = "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation2 div.MuiInputBase-root input"
        slide_title_input = page.locator(slide_title_id).first
        slide_title_input.clear()
        slide_title_input.fill("")

        # Substituir o conteúdo do campo "HTML Code" com um novo código de incorporação válido
        # Encontramos esse input pois ele está dentro do segundo div com a classe "MuiInputBase-root"
        slide_url_id = "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation2 div.MuiInputBase-root input"
        slide_url_input = page.locator(slide_url_id).nth(1)
        slide_url_input.clear()
        slide_url_input.fill(NEW_HTML_CODE)

        # Clicar em "Salvar Alterações"
        # Encontramos esse botão pois é o único botão com o texto "Salvar Alterações"
        locator = page.locator('button:has-text("Salvar Alterações")')
        expect(locator).to_have_attribute("disabled", "")
        expect(locator).to_be_disabled()


def test_rf009_edit_slide_failed_with_empty_url():
    # Criando um contexto Playwright
    with sync_playwright() as playwright:
        ############################################################
        ########## PRIMEIRA PARTE - INICIALIZAÇÃO E LOGIN ##########
        ############################################################
        # Inicializando o navegador
        browser = playwright.chromium.launch(headless=False, channel=DEFAULT_BROWSER)

        # Carregando as credenciais de login armazenadas e criando uma nova página
        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        ###################################################
        ####### SEGUNDA PARTE - ETAPAS DE EXECUÇÃO ########
        ###################################################
        # Acessar a página de gerenciamento de conteúdo do curso
        page.goto(COURSE_MANAGEMENT_URL)

        # Acessar a página de gerenciamento de conteúdo do curso
        # Para isso, clicamos no primeiro botão com o texto "Gerenciar Curso" na página
        page.click('button:has-text("Gerenciar Curso")')

        # Acessar a aba "Slides"
        page.click('button[role="tab"]:has-text("Slides")')

        # Acessar o ícone "Editar" para os slides "Exemplo 01".
        # Encontramos esse botão pois é o primeiro botão na página com um svg dentro dele.
        page.click('button:has(svg[data-testid="EditIcon"])')

        # Acessar o campo "Título do Slide" e alterá-lo para "".
        # Encontramos esse input pois estamos limpando primeiro e depois preenchendo o campo de título do slide
        slide_title_id = "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation2 div.MuiInputBase-root input"
        slide_title_input = page.locator(slide_title_id).first
        slide_title_input.clear()
        slide_title_input.fill(NEW_SLIDE_TITLE)

        # Acessar o campo "Código HTML" e alterá-lo para um novo código de incorporação válido
        # Encontramos esse input pois ele está dentro do segundo div com a classe "MuiInputBase-root"
        slide_url_id = "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation2 div.MuiInputBase-root input"
        slide_url_input = page.locator(slide_url_id).nth(1)
        slide_url_input.clear()
        slide_url_input.fill("")

        # Clicar em "Salvar Alterações"
        # Verificando se o botão "Salvar Alterações" está desabilitado
        locator = page.locator('button:has-text("Salvar Alterações")')
        expect(locator).to_have_attribute("disabled", "")
        expect(locator).to_be_disabled()
