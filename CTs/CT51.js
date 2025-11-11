const { By, until } = require('selenium-webdriver');

/*
 RF51 – O sistema deve permitir que o estudante acesse materiais extras vinculados ao curso ou à aula correspondente, quando disponíveis.
*/

async function ct51(driver) {

    // IR PARA CURSO
    const courseLink = "https://testes.codefolio.com.br/classes?courseId=-OdUWfHdfVN8eOh2HKzU";
    await driver.executeScript(`window.location.replace('${courseLink}')`);

    // 1. Procura botão de materiais extras
    let links = await driver.findElement(By.xpath("//button[text()='Materiais Extras']"));

    // clica no botão de materiais extras
    await links.click();

    // Procura links de materiais extras
    let materialLink = await driver.findElement(By.xpath("//a[text()='Acessar Material']"));
    
    // Clica no primeiro material extra
    await materialLink.click();
}

module.exports = { ct51 };