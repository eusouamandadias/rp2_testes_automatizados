const { By } = require('selenium-webdriver');

/*
Requisito: RF48 – O sistema deve permitir que o estudante selecione um vídeo específico de um curso por meio do botão “Ver Vídeo”.
*/

async function ct48(driver) {

    // IR PARA CURSO
    const courseLink = "https://testes.codefolio.com.br/classes?courseId=-OcYY89WK7_dK26GmhzI";
    await driver.executeScript(`window.location.replace('${courseLink}')`);

    try{
        await driver.findElement(By.xpath("//button[contains(.,'Ver Vídeo')]")).click();
        console.log("Botão clicado!")
    }catch(e){
        console.error("Não foi possível clicar no botão!", e)
    }


}

module.exports = { ct48 };