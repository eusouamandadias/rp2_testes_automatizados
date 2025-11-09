"""
This module contains tests for the Functional Requirement 009 (RF009) of Codefolio project.

Requirement: RF9 – The system must allow editing information or replacing already registered slides.

Objective: Verify if the teacher can change the title or replace the HTML code of an existing slide lesson.

Precondition:
- User authenticated as teacher.
- Be on the editing/content page of a course that has a registered slide lesson.

Execution steps:
    01. Access the course content management page.
    02. Access a course management page that contains slide lessons.
    03. Access the "Slides" tab.
    04. Click on the "Edit" icon for the slides "Introdução ao Playwright".
    05. Change the "Slide Title" field to "Lição 1 - Preparando o ambiente para testar com Playwright".
    06. Replace the content of the "HTML Code" field with a new valid embed code.
    07. Click "Save Changes".

Input Data (when applicable):
    1. Title: "Lição 1 - Preparando o ambiente para testar com Playwright"
    2. HTML Code: (Ex: <iframe src="https://docs.google.com/presentation/d/e/NEW-LINK..."></iframe>)

Expected Result: The system should display the message "The slide was successfully updated!" and the lesson should appear in the list with the new title and link.
"""

# Importing libraries
from playwright.sync_api import sync_playwright, expect

# Importing utility functions
from tests.utils import load_credentials


# Defining constants for RF009 test
DEFAULT_BROWSER = "chrome"  # Options: "chrome", "chromium", "firefox", "webkit"
BASE_URL = "https://testes.codefolio.com.br"
COURSE_MANAGEMENT_URL = f"{BASE_URL}/manage-courses"  # Execution Step 01
NEW_SLIDE_TITLE = (
    "Lição 1 - Preparando o ambiente para testar com Playwright"  # Execution Step 05
)
NEW_HTML_CODE = "https://docs.google.com/presentation/d/e/2PACX-1vSzcPobWyEazwXnAFux9eVqLFBMeC3yQuKbRvpgRO2OsAv34A4BJWfAXLfsDPl2vNYeUATNdVwnI4LI/pubembed?start=false&loop=false&delayms=30000"  # Execution Step 06
MESSAGE_TEXT = "O slide foi atualizado com sucesso!"


def test_rf009_edit_slide_success():
    # Creating a Playwright context
    with sync_playwright() as playwright:
        ############################################################
        #### TEST SOURCE CODE PART 1 - Initialization and Login ####
        ############################################################
        # Initializing the browser
        browser = playwright.chromium.launch(headless=False, channel=DEFAULT_BROWSER)

        # Loading stored login credentials and creating a new page
        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        ###################################################
        #### TEST SOURCE CODE PART 2 - EXECUTION STEPS ####
        ###################################################
        # Performing Execution Step 01: Access the course content management page
        page.goto(COURSE_MANAGEMENT_URL)

        # Performing Execution Step 02: Access a course management page that contains slide lessons
        # To do so, we click on the first button with the text "Gerenciar Curso" on the page
        # <button class="MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary css-emcv54" tabindex="0" type="button" id=":r1c:">Gerenciar Curso<span class="MuiTouchRipple-root css-4mb1j7"></span></button>
        page.click('button:has-text("Gerenciar Curso")')

        # Performing Execution Step 03: Access the "Slides" tab
        page.click('button[role="tab"]:has-text("Slides")')

        # Performing Execution Step 04: Click on the "Edit" icon for the slides "Introdução ao Playwright".
        # We find this button as it is the first button on the page with a svg inside it.
        page.click('button:has(svg[data-testid="EditIcon"])')

        # Performing Execution Step 05: Change the "Slide Title" field to "Lesson 2 - Scrum and Kanban".
        # We find this input by clearing first and then filling the slide title field
        slide_title_id = "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation2 div.MuiInputBase-root input"
        slide_title_input = page.locator(slide_title_id).first
        slide_title_input.clear()
        slide_title_input.fill(NEW_SLIDE_TITLE)

        # Performing Execution Step 06: Replace the content of the "HTML Code" field with a new valid embed code
        # We find this input as it is inside of the second div with class "MuiInputBase-root"
        slide_url_id = "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation2 div.MuiInputBase-root input"
        slide_url_input = page.locator(slide_url_id).nth(1)
        slide_url_input.clear()
        slide_url_input.fill(NEW_HTML_CODE)

        # Performing Execution Step 07: Click "Save Changes"
        # We find this button as it is the only button with the text "Salvar Alterações"
        page.click('button:has-text("Salvar Alterações")')

        # Verifying that the success message is displayed
        dialog = page.get_by_role("dialog")
        expect(dialog).to_be_visible()
        msg = dialog.get_by_text(MESSAGE_TEXT, exact=True)
        expect(msg).to_be_visible()
        expect(msg).to_have_text(MESSAGE_TEXT)


def test_rf009_edit_slide_failed_with_empty_title():
    # Creating a Playwright context
    with sync_playwright() as playwright:
        ############################################################
        #### TEST SOURCE CODE PART 1 - Initialization and Login ####
        ############################################################
        # Initializing the browser
        browser = playwright.chromium.launch(headless=False, channel=DEFAULT_BROWSER)

        # Loading stored login credentials and creating a new page
        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        ###################################################
        #### TEST SOURCE CODE PART 2 - EXECUTION STEPS ####
        ###################################################
        # Performing Execution Step 01: Access the course content management page
        page.goto(COURSE_MANAGEMENT_URL)

        # Performing Execution Step 02: Access a course management page that contains slide lessons
        # To do so, we click on the first button with the text "Gerenciar Curso" on the page
        page.click('button:has-text("Gerenciar Curso")')

        # Performing Execution Step 03: Access the "Slides" tab
        page.click('button[role="tab"]:has-text("Slides")')

        # Performing Execution Step 04: Click on the "Edit" icon for the slides "Exemplo 01".
        # We find this button as it is the first button on the page with a svg inside it.
        page.click('button:has(svg[data-testid="EditIcon"])')

        # Performing Execution Step 05: Change the "Slide Title" field to "".
        # We find this input by clearing first and then filling the slide title field
        slide_title_id = "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation2 div.MuiInputBase-root input"
        slide_title_input = page.locator(slide_title_id).first
        slide_title_input.clear()
        slide_title_input.fill("")

        # Performing Execution Step 06: Replace the content of the "HTML Code" field with a new valid embed code
        # We find this input as it is inside of the second div with class "MuiInputBase-root"
        slide_url_id = "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation2 div.MuiInputBase-root input"
        slide_url_input = page.locator(slide_url_id).nth(1)
        slide_url_input.clear()
        slide_url_input.fill(NEW_HTML_CODE)

        # Performing Execution Step 07: Click "Save Changes"
        # We find this button as it is the only button with the text "Salvar Alterações"
        page.click('button:has-text("Salvar Alterações")')

        # Verifying that the "Save Changes" button is disabled

        locator = page.locator('button:has-text("Salvar Alterações")')
        expect(locator).to_be_disabled()


def test_rf009_edit_slide_failed_with_empty_url():
    # Creating a Playwright context
    with sync_playwright() as playwright:
        ############################################################
        #### TEST SOURCE CODE PART 1 - Initialization and Login ####
        ############################################################
        # Initializing the browser
        browser = playwright.chromium.launch(headless=False, channel=DEFAULT_BROWSER)

        # Loading stored login credentials and creating a new page
        credentials = load_credentials(playwright=playwright, browser=browser)
        page = credentials["page"]

        ###################################################
        #### TEST SOURCE CODE PART 2 - EXECUTION STEPS ####
        ###################################################
        # Performing Execution Step 01: Access the course content management page
        page.goto(COURSE_MANAGEMENT_URL)

        # Performing Execution Step 02: Access a course management page that contains slide lessons
        # To do so, we click on the first button with the text "Gerenciar Curso" on the page
        # <button class="MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-colorPrimary css-emcv54" tabindex="0" type="button" id=":r1c:">Gerenciar Curso<span class="MuiTouchRipple-root css-4mb1j7"></span></button>
        page.click('button:has-text("Gerenciar Curso")')

        # Performing Execution Step 03: Access the "Slides" tab
        page.click('button[role="tab"]:has-text("Slides")')

        # Performing Execution Step 04: Click on the "Edit" icon for the slides "Exemplo 01".
        # We find this button as it is the first button on the page with a svg inside it.
        page.click('button:has(svg[data-testid="EditIcon"])')

        # Performing Execution Step 05: Change the "Slide Title" field to "".
        # We find this input by clearing first and then filling the slide title field
        slide_title_id = "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation2 div.MuiInputBase-root input"
        slide_title_input = page.locator(slide_title_id).first
        slide_title_input.clear()
        slide_title_input.fill(NEW_SLIDE_TITLE)

        # Performing Execution Step 06: Replace the content of the "HTML Code" field with a new valid embed code
        # We find this input as it is inside of the second div with class "MuiInputBase-root"
        slide_url_id = "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation2 div.MuiInputBase-root input"
        slide_url_input = page.locator(slide_url_id).nth(1)
        slide_url_input.clear()
        slide_url_input.fill("")

        # Performing Execution Step 07: Click "Save Changes"
        # We find this button as it is the only button with the text "Salvar Alterações"
        page.click('button:has-text("Salvar Alterações")')

        # Verifying that the "Save Changes" button is disabled

        locator = page.locator('button:has-text("Salvar Alterações")')
        expect(locator).to_be_disabled()
