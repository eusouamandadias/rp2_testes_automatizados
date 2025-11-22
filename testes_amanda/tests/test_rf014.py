"""
Este módulo contém os testes referentes ao Requisito Funcional 013 (RF014) do projeto Codefolio.

Requisito: RF14 – O sistema deve permitir excluir materiais extras, removendo o acesso dos alunos a esses recursos.

"""
# Importando bibliotecas necessárias
from re import A, T
from time import time
from playwright.sync_api import sync_playwright, expect

# Importando funções utilitárias
from tests.utils import DEFAULT_BROWSER, load_credentials


# Definindo constantes para o teste RF014
BROWSER_PADRAO = "chrome"  # Opções: "chrome", "chromium", "firefox", "webkit"
URL_BASE = "https://testes-codefolio.web.app"
URL_GERENCIAMENTO_CURSOS = f"{URL_BASE}/manage-courses"
TEMPO_DE_PAUSA = 3000
