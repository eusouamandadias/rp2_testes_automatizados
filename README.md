# Automação de Testes com Playwright

Este projeto concentra testes automatizados utilizando a biblioteca Playwright.

Os testes acessam o seguinte website:

- CODEFÓLIO - https://testes.codefolio.com.br/

O Playwright é uma biblioteca que permite a automação de navegadores web para testes de interface do usuário. Ele suporta múltiplos navegadores, incluindo Chromium, Firefox e WebKit, e oferece uma API simples para interagir com elementos da página, navegar entre páginas, preencher formulários, capturar screenshots, entre outras funcionalidades.

O Playwright possui interface com várias linguagens de programação. Nesse projeto, utilizamos a interface para Python.

## Requisitos

Os testes desse projeto foram voltados à validação dos seguintes requisitos:

- **Requisito 001:** Verificar se uma mensagem de erro é exibida ao tentar realizar login com credenciais inválidas.
- **Requisito 002:** Verificar se o sistema permite o login com credenciais válidas.

## Estrutura do Projeto

O projeto está estruturado da seguinte forma:

```
.
├── README.md
├── poetry.lock
├── pyproject.toml
├── report.html
└── tests
    ├── requirement_001.py
    └── requirement_002.py
```

Aqui está uma descrição dos principais arquivos e diretórios:

- `README.md`: Este arquivo, que contém informações sobre o projeto.
- `poetry.lock`: Arquivo gerado pelo Poetry que registra as versões exatas das dependências instaladas.
- `pyproject.toml`: Arquivo de configuração do Poetry que define as dependências do projeto e outras configurações.
- `report.html`: Relatório gerado após a execução dos testes.
- `tests/`: Diretório que contém os arquivos de teste para os requisitos especificados.
  - `requirement_001.py`: Teste automatizado para o Requisito 001.
  - `requirement_002.py`: Teste automatizado para o Requisito 002.
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
