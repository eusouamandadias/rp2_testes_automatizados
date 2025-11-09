"""
This module contains tests for the Functional Requirement 010 (RF010) of Codefolio project.

Requirement: RF10 – The system must allow deleting slides from a course, removing the material and its references.

Objective: Verify if the system removes a slide lesson from the course structure when requested by the teacher.

Precondition:
User authenticated with "teacher" profile.
Be on the edit/content page of a course that has a slide lesson.

Execution steps:
    01. Access the course content management page.
    02. Access the Testes Automatizados com Playwright course management page (click the "Gerenciar Curso" button).
    03. Access the course slides tab.
    04. Locate the "Lição 1 - Preparando o ambiente para testar com Playwright" slides.
    05. Click on the trash can icon.
    06. The system must display a confirmation modal (e.g., "Are you sure you want to delete "Lição 1 - Preparando o ambiente para testar com Playwright"?").
    07. Click "delete".

Input Data (when applicable):
N/A (Confirmation action).

Expected Result: The system must display the message "Slide deleted successfully" and the item "Lição 1 - Preparando o ambiente para testar com Playwright" must no longer be listed in the course content.
"""

# Importing libraries
from playwright.sync_api import sync_playwright, expect

# Importing utility functions
from tests.utils import load_credentials


# Defining constants for RF009 test
DEFAULT_BROWSER = "chrome"  # Options: "chrome", "chromium", "firefox", "webkit"
BASE_URL = "https://testes.codefolio.com.br"
COURSE_MANAGEMENT_URL = f"{BASE_URL}/manage-courses"  # Execution Step 01
SLIDE_LESSON_TITLE = "Lição 1 - Preparando o ambiente para testar com Playwright"
MODAL_CONFIRMATION_TEXT = f'Você tem certeza que deseja excluir "{SLIDE_LESSON_TITLE}"?'


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

        # Performing Execution Step 04: Click on the "Delete" icon for the slides "Lição 1 - Preparando o ambiente para testar com Playwright".
        page.click('button:has(svg[data-testid="DeleteIcon"])')

        # Performing Execution Step 05: Confirm the deletion
        page.click('button:has-text("Excluir")')

        # Validating the Expected Result
        # The system must display the message "Você tem certeza que deseja excluir "Lição 1 - Preparando o ambiente para testar com Playwright?"?"
        expect(page.locator('div[role="dialog"]')).to_have_text(MODAL_CONFIRMATION_TEXT)
