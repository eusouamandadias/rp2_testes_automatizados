const { By, until } = require('selenium-webdriver');

/*
RF52 –O sistema deve permitir que o estudante acesse quizzes que estejam desbloqueados em um curso.
*/

async function ct(driver) {

    // IR PARA CURSO
    const courseLink = "https://testes.codefolio.com.br/classes?courseId=-OdUWfHdfVN8eOh2HKzU";
    await driver.executeScript(`window.location.replace('${courseLink}')`);

    // 1. Procura botão de fazer quiz
    let links = await driver.findElement(By.xpath("//button[text()='Fazer Quiz']"));

    // clica no botão de fazer quiz
    await links.click();
}

module.exports = { ct };