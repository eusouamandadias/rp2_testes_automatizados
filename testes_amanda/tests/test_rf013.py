"""
Este módulo contém os testes referentes ao Requisito Funcional 013 (RF013) do projeto Codefolio.

Requisito: RF13 – O sistema deve permitir excluir materiais extras, removendo o acesso dos alunos a esses recursos.

"""
# Importando bibliotecas necessárias
from re import A, T
from time import time
from playwright.sync_api import sync_playwright, expect

# Importando funções utilitárias
from tests.utils import DEFAULT_BROWSER, load_credentials


# Definindo constantes para o teste RF013
BROWSER_PADRAO = "chrome"  # Opções: "chrome", "chromium", "firefox", "webkit"
URL_BASE = "https://testes-codefolio.web.app"
URL_GERENCIAMENTO_CURSOS = f"{URL_BASE}/manage-courses"
TITULO_MATERIAL_EXTRA = "Get Started with Playwright and VS Code (2025 edition)"
URL_MATERIAL_EXTRA = "https://www.youtube.com/watch?v=WvsLGZnHmzw&t=909s"
TEMPO_DE_PAUSA = 3000


def test_rf013_excluir_material_extra_com_sucesso():
    with sync_playwright() as playwright:  # Defining Playwright context
        ############################################################
        ########## FIRST PART - INITIALIZATION AND LOGIN ###########
        ############################################################
        browser = playwright.chromium.launch(headless=False, channel=BROWSER_PADRAO)
        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        # Navigating to course management page
        page.goto(URL_GERENCIAMENTO_CURSOS)
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        # Opening course card for "Testes Automatizados com Playwright"
        page.locator(".MuiCard-root").filter(
            has_text="Testes Automatizados com Playwright"
        ).get_by_role("button", name="Gerenciar Curso").click()

        # Selecting "Materiais Extras" tab
        page.click('button[role="tab"]:has-text("Materiais Extras")')
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        # Locating all materials with the expected title
        materiais = page.locator(".MuiListItem-root").filter(
            has_text="Get Started with Playwright and VS Code (2025 edition)"
        )
        quantidade_mesmos_materiais_antes = materiais.count()

        print(f"\n\nQuantidade materiais antes: {quantidade_mesmos_materiais_antes}")
        ############################################################
        ########## GARANTINDO MATERIAL PARA EXCLUSÃO ###############
        ############################################################
        if quantidade_mesmos_materiais_antes == 0:
            nome_material_extra = page.get_by_label("Nome do Material")
            nome_material_extra.fill(TITULO_MATERIAL_EXTRA)

            url_material_extra = page.get_by_label("URL do Material")
            url_material_extra.fill(URL_MATERIAL_EXTRA)

            page.wait_for_timeout(TEMPO_DE_PAUSA)

            page.click('button:has-text("Adicionar Material")', timeout=10000)

            expect(page.locator('button:has-text("OK")')).to_be_visible()
            page.wait_for_timeout(TEMPO_DE_PAUSA)
            page.click('button:has-text("OK")', timeout=10000)

            page.wait_for_timeout(TEMPO_DE_PAUSA)
            materiais = page.locator(".MuiListItem-root").filter(
                has_text="Get Started with Playwright and VS Code (2025 edition)"
            )
            quantidade_mesmos_materiais_antes = materiais.count()
            print(f"Quantidade depois de criar: {quantidade_mesmos_materiais_antes}")
            assert quantidade_mesmos_materiais_antes >= 1

        ############################################################
        ########## EXCLUINDO O PRIMEIRO MATERIAL ENCONTRADO ########
        ############################################################
        primeiro_material = materiais.first
        expect(primeiro_material).to_be_visible()

        primeiro_material.locator('button:has(svg[data-testid="DeleteIcon"])').click()

        page.wait_for_timeout(TEMPO_DE_PAUSA)

        confirmar_exclusao = page.get_by_role("button", name="Sim, Excluir")
        expect(confirmar_exclusao).to_be_visible()
        confirmar_exclusao.click()

        expect(page.get_by_text("Material excluído com sucesso!")).to_be_visible(
            timeout=15000
        )
        print("Material excluído com sucesso!")

        ############################################################
        ########## VALIDANDO A QUANTIDADE APÓS EXCLUSÃO ############
        ############################################################
        page.wait_for_timeout(TEMPO_DE_PAUSA)

        materiais_depois = page.locator(".MuiListItem-root").filter(
            has_text="Get Started with Playwright and VS Code (2025 edition)"
        )
        quantidade_mesmos_materiais_depois = materiais_depois.count()

        assert (
            quantidade_mesmos_materiais_depois == quantidade_mesmos_materiais_antes - 1
        )

        print(f"\n\nQuantidade materiais final: {quantidade_mesmos_materiais_depois}")
