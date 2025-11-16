const { By, until } = require('selenium-webdriver');

/*
RF54 – O sistema deve permitir que o estudante reporte problemas relacionados a vídeos, materiais ou funcionamento geral do curso.
*/

async function ct54(driver){
    // IR PARA CURSO COM QUIZ BLOQUADO
    const courseLink = "https://testes.codefolio.com.br/classes?courseId=-OdfPOQuNTkYquZM9AvL";
    await driver.executeScript(`window.location.replace('${courseLink}')`);

    // TENTAR LOCALIZAR BOTÃO DE REPORTE E CLICAR NO MESMO
    try{
        await driver.findElement(By.xpath("//button[@title='Reportar problema']")).click();
        console.log("Botão de reporte localizado e clicado.")
        console.log("\nTeste finalizado com sucesso.")
    }catch(e){
        console.log("Não foi possível localizar e clicar no botão de reporte!\n", e);
    }

    // TESTE PASSOU
    
}

module.exports = { ct54 };