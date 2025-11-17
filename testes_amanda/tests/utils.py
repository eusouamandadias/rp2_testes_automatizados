"""
This module hosts a set of utility functions for tests.

It includes common operations such as logging in and storing credentials.

The main purpose of this module is to promote code reuse and maintainability across different test cases.
"""
# Importing libraries
import os
import shutil
import time
from playwright.sync_api import sync_playwright

# Defining constants for the utility functions
DEFAULT_BROWSER = "chrome"  # Options: "chrome", "chromium", "firefox", "webkit"
DOMAIN = "https://testes.codefolio.com.br"
LOGIN_URL = f"{DOMAIN}/login"
RELOAD_INTERVAL = 1800  # Time in ms to force reload credentials (30 minutes)
TIME_TO_LOGIN = 20000  # Time in ms to wait for manual login (20 seconds)


def load_credentials(playwright, browser):
    # Creating an auxiliary file to store the last time the credentials were loaded
    if not os.path.exists("force_reload.txt"):
        with open("force_reload.txt", "w") as f:
            f.write("0")

    # Checking if the credentials need to be reloaded (every 30 minutes by default).
    # If so, we remove the existing login state directory (.google-chrome-config),
    # create a new one, update the timestamp, and finally stop the entire
    # test execution to ensure that new credentials are used in the next test run
    with open("force_reload.txt", "r") as f:
        last_loaded = float(f.read().strip())
    current_time = time.time()
    must_reload = current_time - last_loaded > RELOAD_INTERVAL
    if must_reload:
        # Removing the directory that stores the login state (.google-chrome-config)
        shutil.rmtree(".google-chrome-config")

    # Launching a persistent browser context with the stored login state
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=".google-chrome-config",
        channel="chrome",
        headless=False,
        args=["--profile-directory=Default"],
    )
    page = context.pages[0] if context.pages else context.new_page()

    # Updating the timestamp
    with open("force_reload.txt", "w") as f:
        f.write(str(current_time))

    if must_reload:
        # Accessing the login page
        page.goto(LOGIN_URL)

        # Acessing the button that opens the login option
        page.click('button[id=":r0:"]')

        # Waiting for manual login before storing the credentials
        page.wait_for_url(f"**{DOMAIN}**", timeout=TIME_TO_LOGIN)

        # Closing the browser
        browser.close()

        print("\n\nPlease restart the test to use the updated credentials.\n\n")
        exit(0)

    return {"context": context, "page": page}
