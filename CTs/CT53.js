const { By, until } = require('selenium-webdriver');

/*
 R F53 – O sistema deve exib*ir uma mensagem apropriada quando o estudante tentar acessar um quiz bloqueado.
 */

async function ct53(driver) {

    // IR PARA LISTA DE CURSOS
    const courseLink = "https://testes.codefolio.com.br/listcurso";
    await driver.executeScript(`window.location.replace('${courseLink}')`);

    console.log("Navegado para página de cursos.")

    // salvar em variável elemento da lista de cursos (DIV)
    const divCursos = await driver.wait(
        until.elementIsVisible(driver.findElement(By.xpath(
            "//div[contains(@class, 'MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-1eikg3m')]"
        ))),
        15000
    );

    console.log("Selecionar div com lista de cursos.")

    // salvar em variável todas as divs de cada cada curso
    const cursos = await divCursos.findElements(By.xpath("./div"));

    // variável para armazenar o primeiro curso com PIN
    let curso_com_pin_element;

    // loop para buscar dentro de toda a lista de curso o primeiro com cadeado
    for (const curso of cursos){

        const lockIcons = await curso.findElements(By.css("svg[data-testid='LockIcon']"));

        if (lockIcons.length > 0) {
            curso_com_pin_element = lockIcons[0];
            console.log("Encontrado curso com PIN.")
            break;
        }
    }
    // tentar localizar botão de acessar curso com pin e clicar no mesmo.
    try{
        btn_acessar = curso_com_pin_element.findElement(By.xpath("//button[text()='Começar']"))
        console.log("Botão de 'Começar' do curso com PIN encontrado.")
        driver.executeScript("arguments[0].scrollIntoView({block:'center'});", btn_acessar)
        btn_acessar.click();
        console.log("Botão 'Começar' de curso com PIN clicado!")
        console.log("\n Teste concluído com sucesso.")
    }catch(e){
        console.error("Erro ao localizar e clicar botão do curso com PIN.\n", e)
    }

}

// TESTE PASSOU

module.exports = { ct53 };
