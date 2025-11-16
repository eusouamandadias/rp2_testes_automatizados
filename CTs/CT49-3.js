const { By, until, error } = require('selenium-webdriver');

/*
 RF49  – O sistema deve permitir que o estudante acesse, assista e avance vídeos de um curso.

 CT49-3 curso sem quiz obrigatório e apenas um vídeo = clicar no botão próximo não muda de vídeo, pois botão próximo não foi carregado.

 */

async function ct(driver) {

    // IR PARA CURSO
    const courseLink = "https://testes.codefolio.com.br/classes?courseId=-OeCxLJS3PwL44BB-J-L";

    await driver.executeScript(`window.location.replace('${courseLink}')`);

    try{
        // variáveis de elementos
        const iframeLocator = By.xpath("//iframe[contains(@id, 'widget')]");
        const playButton = By.css('.ytp-large-play-button');
        const NextButton = By.css('.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-1dv06w3');

        const iframeId = await driver.findElement(iframeLocator).getAttribute('id')

        // alternar para iframe
        await driver.switchTo().frame(driver.findElement(iframeLocator));
        console.log("Iframe selecionado")
   
        // clicar no botão de play do youtube
        await driver.findElement(playButton).click();
        console.log("Youtube button clicado")

        await driver.sleep(5000);

        // sair da seleção do Iframe
        await driver.switchTo().defaultContent();
        console.log("Iframe removido da seleção!")

        await driver.sleep(5000);

        // clicar no botão próximo
        console.log("Aguardando o botão 'próximo' ficar visível...");
        try{
            const nextButton = await driver.wait(until.elementLocated(NextButton), 10000);
            await driver.wait(until.elementIsVisible(nextButton), 10000).click();
            console.log("Botão 'próximo' clicado!");

            try{
                // alternar para iframe
                 const iframeId2 = await driver.wait(until.elementLocated(iframeLocator), 10000).getAttribute('id');
                if (iframeId2 == iframeId){
                    throw new error("Não foi encontrado um segundo vídeo! Possível quiz bloqueado ou vídeo inexistente")
                }
                await driver.switchTo().frame(driver.findElement(iframeLocator));
               

                console.log("Segundo Iframe selecionado")
                console.log("Teste finalizado com sucesso.")
            }catch(e){
                console.error("Não foi encontrado vídeo!", e);
            }
        }catch(e){
            console.error("Não foi possível localizar o botão 'próximo'.\n", e)
        }
        


    }catch(e){
        console.error("Erro ao clicar!", e)
    }
  
}

    // TESTE FALHOU

module.exports = { ct };
