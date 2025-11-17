# Automação de Testes com Playwright

Este projeto concentra testes automatizados utilizando a biblioteca Playwright.

Os testes acessam o seguinte website:

- [CODEFÓLIO] (https://testes.codefolio.com.br)

O Playwright é uma biblioteca que permite a automação de navegadores web para testes de interface do usuário. Ele suporta múltiplos navegadores, incluindo Chromium, Firefox e WebKit, e oferece uma API simples para interagir com elementos da página, navegar entre páginas, preencher formulários, capturar screenshots, entre outras funcionalidades.

O Playwright possui interface com várias linguagens de programação. Nesse projeto, utilizamos a interface para Python.

## Requisitos

Os testes desse projeto foram voltados à validação dos seguintes requisitos:

- **Requisito 009 -** Edição de Slides: O sistema deve permitir editar informações ou substituir slides já cadastrados.
- **Requisito 010 -** Exclusão de Slides: O sistema deve permitir excluir slides de um curso, removendo o material e suas referências.
- **Requisito 011 -** Cadastro de Material Extra: O sistema deve permitir o vínculo de materiais extras (como links para PDFs, planilhas ou outros) a aulas (slides ou vídeos)específicos.
- **Requisito 012 -** Edição de Material Extra: O sistema deve permitir editar o nome, descrição e vínculo de materiais extras já cadastrados.
- **Requisito 013 -** Exclusão de Material Extra: O sistema deve permitir excluirmateriais extras, removendo o acesso dos alunos a esses recursos.
- **Requisito 014 -** Cadastro de Quiz: O sistema deve permitir criar quizzes, definindo título, perguntas, alternativas e resposta correta.
- **Requisito 015 -** Edição de Quiz: O sistema deve permitir editar quizzes existentes, alterando perguntas, respostas e alternativa correta.
- **Requisito 016 -** Exclusão de Quiz: O sistema deve permitir excluir quizzes e suas respectivas perguntas

## Estrutura do Projeto

O projeto está estruturado da seguinte forma:

```
.
├── README.md
├── poetry.lock
├── pyproject.toml
├── report.html
└── tests
    ├── test_rf009.py
    └── test_rf010.py
```

Aqui está uma descrição dos principais arquivos e diretórios:

- `README.md`: Este arquivo, que contém informações sobre o projeto.
- `poetry.lock`: Arquivo gerado pelo Poetry que registra as versões exatas das dependências instaladas.
- `pyproject.toml`: Arquivo de configuração do Poetry que define as dependências do projeto e outras configurações.
- `report.html`: Relatório gerado após a execução dos testes.
- `tests/`: Diretório que contém os arquivos de teste para os requisitos especificados.
  - `test_rf009.py`: Teste automatizado para o Requisito 009.
  - `test_rf010.py`: Teste automatizado para o Requisito 010.
  - `...`: Outros arquivos de teste conforme necessário.

## Como Instalar o Projeto

1. Clone o repositório do projeto para o seu ambiente local.

   - `git clone <URL_DO_REPOSITORIO>`

2. Navegue até o diretório do projeto.

   - `cd <NOME_DO_DIRETORIO>`

3. Instale o Poetry, caso ainda não o tenha instalado.

   - Siga as instruções oficiais em https://python-poetry.org/docs/#installation

4. Instale as dependências do projeto.

   - `poetry install`

5. Entre no ambiente virtual criado pelo Poetry.
   - `poetry env activate` ou `poetry_shell` caso tenha configurado um alias para o comando.

## Como Executar os Testes

Estando no ambiente virtual do Poetry, podemos executar os testes utilizando vários comandos. Abaixo estão alguns exemplos.

1. Executar todos os casos de teste dentro de um arquivo específico:

   - `pytest tests/<NOME_DO_ARQUIVO>.py -v --html=report.html --self-contained-html`

2. Executar somente um caso de teste específico dentro de um arquivo:

   - `pytest tests/<NOME_DO_ARQUIVO>.py::<NOME_DA_FUNCAO_DE_TESTE> -v --html=report.html --self-contained-html`

3. Executar todos os casos de teste do projeto:

   - `pytest tests/ -v --html=report.html --self-contained-html`

4. O pytest oculta as saídas de print dos testes que são bem-sucedidos por padrão.NV Para visualizar essas saídas, utilize a opção:
   - `pytest -s tests/test_rf009.py -k <NOME_DA_FUNCAO_DE_TESTE>`
