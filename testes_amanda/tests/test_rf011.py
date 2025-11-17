"""
Este módulo contém os testes referentes ao Requisito Funcional 011 (RF011) do projeto Codefolio.

Requisito: RF11 – O sistema deve permitir o vínculo de materiais extras (como links para PDFs, planilhas ou outros) a aulas (slides ou vídeos) específicos.

"""
# Importando bibliotecas necessárias
from re import A, T
from time import time
from playwright.sync_api import sync_playwright, expect

# Importando funções utilitárias
from tests.utils import DEFAULT_BROWSER, load_credentials

BROWSER_PADRAO = "chrome"  # Opções: "chrome", "chromium", "firefox", "webkit"
URL_BASE = "https://testes.codefolio.com.br"
URL_GERENCIAMENTO_CURSOS = f"{URL_BASE}/manage-courses"
TITULO_MATERIAL_EXTRA = "Get Started with Playwright and VS Code (2025 edition)"
URL_MATERIAL_EXTRA = "https://www.youtube.com/watch?v=WvsLGZnHmzw&t=909s"
TEMPO_DE_PAUSA = 3000

# =================
# ===== CT011-1 ====
# =================
def teste_rf011_adicionar_material_extra_com_sucesso():
    with sync_playwright() as playwright:
        # Inicializando o navegador
        browser = playwright.chromium.launch(headless=False, channel=BROWSER_PADRAO)

        # Carregando credenciais de login armazenadas e criando uma nova página
        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        page.wait_for_timeout(TEMPO_DE_PAUSA)
        # Accessar a página de gerenciamento de conteúdo do curso
        print("\n\nIndo para a página de gerenciamento de cursos...\n")
        page.goto(URL_GERENCIAMENTO_CURSOS)

        page.wait_for_timeout(TEMPO_DE_PAUSA)
        # Navegar até a aba de Materiais Extras
        page.locator(".MuiCard-root").filter(
            has_text="Testes Automatizados com Playwright"
        ).get_by_role("button", name="Gerenciar Curso").click()
        page.click('button[role="tab"]:has-text("Slides")')

        page.click('button[role="tab"]:has-text("Materiais Extras")')
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        nome_material_extra = page.get_by_label("Nome do Material")
        nome_material_extra.fill(TITULO_MATERIAL_EXTRA)

        url_material_extra = page.get_by_label("URL do Material")
        url_material_extra.fill(URL_MATERIAL_EXTRA)
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        page.click('button:has-text("Adicionar Material")', timeout=10000)
        expect(page.locator('button:has-text("OK")')).to_be_visible()
        page.wait_for_timeout(TEMPO_DE_PAUSA)
        page.click('button:has-text("OK")')

        lista_materiais = page.get_by_role("list")
        expect(lista_materiais).to_contain_text(TITULO_MATERIAL_EXTRA)


# =================
# ===== CT11-2 ====
# =================
def test_rf011_adicionar_material_extra_com_falha_campos_vazios():
    with sync_playwright() as playwright:
        # Inicializando o navegador
        browser = playwright.chromium.launch(headless=False, channel=BROWSER_PADRAO)

        # Carregando credenciais de login armazenadas e criando uma nova página
        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        page.wait_for_timeout(TEMPO_DE_PAUSA)
        # Accessar a página de gerenciamento de conteúdo do curso
        print("\n\nIndo para a página de gerenciamento de cursos...\n")
        page.goto(URL_GERENCIAMENTO_CURSOS)

        page.wait_for_timeout(TEMPO_DE_PAUSA)
        # Navegar até a aba de Materiais Extras
        page.locator(".MuiCard-root").filter(
            has_text="Testes Automatizados com Playwright"
        ).get_by_role("button", name="Gerenciar Curso").click()
        page.click('button[role="tab"]:has-text("Slides")')

        page.click('button[role="tab"]:has-text("Materiais Extras")')
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        nome_material_extra = page.get_by_label("Nome do Material")
        nome_material_extra.fill("")

        url_material_extra = page.get_by_label("URL do Material")
        url_material_extra.fill("")
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        page.click('button:has-text("Adicionar Material")')
        expect(
            page.locator('text="Preencha o nome e a URL do material"')
        ).to_be_visible()


# =================
# ===== CT11-3 ====
# =================
def teste_rf011_adicionar_material_extra_apenas_com_nome():
    with sync_playwright() as playwright:
        # Inicializando o navegador
        browser = playwright.chromium.launch(headless=False, channel=BROWSER_PADRAO)

        # Carregando credenciais de login armazenadas e criando uma nova página
        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        page.wait_for_timeout(TEMPO_DE_PAUSA)
        # Accessar a página de gerenciamento de conteúdo do curso
        print("\n\nIndo para a página de gerenciamento de cursos...\n")
        page.goto(URL_GERENCIAMENTO_CURSOS)

        page.wait_for_timeout(TEMPO_DE_PAUSA)
        # Navegar até a aba de Materiais Extras
        page.locator(".MuiCard-root").filter(
            has_text="Testes Automatizados com Playwright"
        ).get_by_role("button", name="Gerenciar Curso").click()
        page.click('button[role="tab"]:has-text("Slides")')

        page.click('button[role="tab"]:has-text("Materiais Extras")')
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        nome_material_extra = page.get_by_label("Nome do Material")
        nome_material_extra.fill(TITULO_MATERIAL_EXTRA)

        url_material_extra = page.get_by_label("URL do Material")
        url_material_extra.fill("")
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        page.click('button:has-text("Adicionar Material")')
        expect(
            page.locator('text="Preencha o nome e a URL do material"')
        ).to_be_visible()


# ==================
# ===== CT011-4 ====
# ==================
def teste_rf011_adicionar_material_extra_apenas_com_url():
    with sync_playwright() as playwright:
        # Inicializando o navegador
        browser = playwright.chromium.launch(headless=False, channel=BROWSER_PADRAO)

        # Carregando credenciais de login armazenadas e criando uma nova página
        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        page.wait_for_timeout(TEMPO_DE_PAUSA)
        # Accessar a página de gerenciamento de conteúdo do curso
        print("\n\nIndo para a página de gerenciamento de cursos...\n")
        page.goto(URL_GERENCIAMENTO_CURSOS)

        page.wait_for_timeout(TEMPO_DE_PAUSA)
        # Navegar até a aba de Materiais Extras
        page.locator(".MuiCard-root").filter(
            has_text="Testes Automatizados com Playwright"
        ).get_by_role("button", name="Gerenciar Curso").click()
        page.click('button[role="tab"]:has-text("Slides")')

        page.click('button[role="tab"]:has-text("Materiais Extras")')
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        nome_material_extra = page.get_by_label("Nome do Material")
        nome_material_extra.fill("")

        url_material_extra = page.get_by_label("URL do Material")
        url_material_extra.fill(URL_MATERIAL_EXTRA)
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        page.click('button:has-text("Adicionar Material")')
        expect(
            page.locator('text="Preencha o nome e a URL do material"')
        ).to_be_visible()
