const { By, until } = require('selenium-webdriver');

/*
RF50 – O sistema deve permitir que o estudante navegue entre os vídeos de um curso, utilizando botões de próximo e anterior.
*/

async function ct(driver) {

    // IR PARA CURSO
    const courseLink = "https://testes.codefolio.com.br/classes?courseId=-OdUWfHdfVN8eOh2HKzU";
    await driver.executeScript(`window.location.replace('${courseLink}')`);

    try{
        // variáveis de elementos
        const nextButton = By.xpath("//button[text()='Rever Vídeo']");
        const prevButton = By.css('.css-1dv06w3')


        await driver.sleep(10000);

        // clicar no botão próximo
        await driver.findElement(nextButton).click();
        console.log("NextButton clicado!")

        await driver.sleep(5000);

        // clicar no botão voltar
        await driver.findElement(prevButton).click();
        console.log("PrevButton clicado!")


    }catch(e){
        console.error("Erro ao clicar!", e)
    }
  v

}

module.exports = { ct };