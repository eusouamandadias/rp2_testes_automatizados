const { By, until } = require('selenium-webdriver');

/*
RF55 – O sistema deve permitir que o estudante consulte suas avaliações e notas obtidas nos quizzes e atividades realizadas.
*/

async function ct55(driver) {
    // Navegar para página de avaliações
    const pagina_avaliacoes = "https://testes.codefolio.com.br/minhas-avaliacoes";
    await driver.executeScript(`window.location.replace('${pagina_avaliacoes}')`);

    console.log("Acessando página de avaliações.")

    try{
        // variável que armazena todos os cursos
        const lista = await driver.findElements(By.css(".MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.css-15j76c0"))
        console.log("Carregado lista de avaliações de cada curso.")

        try{
            // loop para listar todos os cursos que tenham ao menos uma avaliação
            let contador = 0;
            for (const element of lista){
                const count = await element.findElement(By.css(".MuiChip-label.MuiChip-labelSmall.css-b9zgoq"))
                if ((await count.getText()).includes("avaliações") && (await count.getText()) != "0 avaliações"){
                    console.log(await count.getText());
                    contador++;
                }
            }
            console.log(`Foram encontrados ${contador} cursos com avaliações.`)
            console.log("\nTeste finalizado!")

        }catch(e){
            console.error("Não foi possível localizar nenhum curso com avaliação.\n", e)
        }
        
    }catch(e){
        console.error("Não foi possível localizar a lista de valiações de cursos.\n", e)
    }
  
    // TESTE FALHOU POIS NÃO CONTABILIZA CURSOS COM 4 AVALIAÇÕES

}

module.exports = { ct55 };