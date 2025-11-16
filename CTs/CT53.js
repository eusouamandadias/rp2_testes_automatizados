const { By, until } = require('selenium-webdriver');

/*
 R F53 – O sistema deve exibir uma mensagem apropriada quando o estudante tentar acessar um quiz bloqueado.
 */

async function ct53(driver) {

    // IR PARA LISTA DE CURSOS
    const courseLink = "https://testes.codefolio.com.br/classes?courseId=-OdfPOQuNTkYquZM9AvL";
    await driver.executeScript(`window.location.replace('${courseLink}')`);

    console.log("Navegado para página de curso com quiz bloqueado.")


    try{
       await driver.findElement(By.xpath("//button[text()='Quiz Bloqueado']")).click();
        console.log("Botão de quiz clicado.")
        console.log("Teste finalizado com sucesso.")
    }catch(e){
        console.log("Erro ao localizar e clicar no botão de quiz!\n", e)
    }

    console.log("\nTeste finalizado!")

}
module.exports = { ct53 };
