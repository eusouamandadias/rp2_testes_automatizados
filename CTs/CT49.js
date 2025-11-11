const { By, until } = require('selenium-webdriver');

/*
 RF49 – O sistema deve permitir que o estudante acesse, assista e avance vídeos de um curso.
*/

async function ct49(driver) {

    // IR PARA CURSO
    const courseLink = "https://testes.codefolio.com.br/classes?courseId=-OdUWfHdfVN8eOh2HKzU";
    await driver.executeScript(`window.location.replace('${courseLink}')`);

    try{
        // variáveis de elementos
        const iframeLocator = By.id('widget2');
        const playButtonLocator = By.css('.ytp-large-play-button');
        const nextButton = By.xpath("//button[text()='Rever Vídeo']");

        // alternar para iframe
        await driver.switchTo().frame(driver.findElement(iframeLocator));
        console.log("Iframe selecionado")
   
        // clicar no botão de play do youtube
        await driver.findElement(playButtonLocator).click();
        console.log("Youtube button clicado")

        await driver.sleep(5000);

        // sair da seleção do Iframe
        await driver.switchTo().defaultContent();
        console.log("Iframe removido da seleção!")

        await driver.sleep(5000);


        // clicar no botão próximo
        await driver.findElement(nextButton).click();
        console.log("NextButton clicado!")


    }catch(e){
        console.log("Erro ao clicar!", e)
    }
  

}

module.exports = { ct49 };