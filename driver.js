const {Builder, Browser} = require('selenium-webdriver');
const {URL, FIREBASE_KEY, FIREBASE_VALUE} = require('./auth');

/**
 * Creates and configures a WebDriver instance.
 * @returns {Promise<import('selenium-webdriver').WebDriver>} A promise that resolves to a WebDriver instance.
 */
async function getDriver() {
  let driver = await new Builder().forBrowser(Browser.CHROME).build();

  await driver.get(URL);
  await driver.manage().window().maximize();

  await driver.manage().setTimeouts({ implicit: 15000 });

  await driver.executeScript(
    "window.localStorage.setItem(arguments[0], arguments[1]);",
    FIREBASE_KEY,
    FIREBASE_VALUE
  );

  await driver.navigate().refresh();

  return driver;
}

module.exports = { getDriver };