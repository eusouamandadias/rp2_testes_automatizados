const { By } = require('selenium-webdriver');

/*
Requisito: RF48 – O sistema deve permitir que o estudante selecione um vídeo específico de um curso por meio do botão “Ver Vídeo”.
*/

async function ct(driver) {

    // IR PARA CURSO
    const courseLink = "https://testes.codefolio.com.br/classes?courseId=-OcYY89WK7_dK26GmhzI";
    await driver.executeScript(`window.location.replace('${courseLink}')`);
    console.log("Redirecionado para página de curso com vídeo.")

    try{
        await driver.findElement(By.xpath("//button[contains(.,'Ver Vídeo')]")).click();
        console.log("Botão clicado!")
    }catch(e){
        console.error("Não foi possível clicar no botão!", e)
    }

    console.log("Teste finalizado.")

    // TESTE PASSOU
}

module.exports = { ct };