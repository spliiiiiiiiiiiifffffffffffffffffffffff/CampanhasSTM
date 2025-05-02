import requests
from integrations.api_clients import StackExchangeAPI
from integrations.api_clients import GitHubAPI

class StackExchangeAPI:
    """Cliente para interagir com a API do Stack Exchange."""
    BASE_URL = "https://api.stackexchange.com/2.3"

    @staticmethod
    def search_questions(query, tags=None, site="stackoverflow"):
        """
        Busca perguntas no Stack Overflow com base em uma query e tags.
        :param query: Termo de busca.
        :param tags: Lista de tags para filtrar os resultados.
        :param site: Site da rede Stack Exchange (padrão: stackoverflow).
        :return: Lista de perguntas.
        """
        params = {
            "order": "desc",
            "sort": "activity",
            "intitle": query,
            "site": site,
        }
        if tags:
            params["tagged"] = ";".join(tags)

        response = requests.get(f"{StackExchangeAPI.BASE_URL}/search", params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            response.raise_for_status()


class GitHubAPI:
    """Cliente para interagir com a API do GitHub."""
    BASE_URL = "https://api.github.com"

    def __init__(self, token=None):
        """
        Inicializa o cliente GitHub.
        :param token: Token de autenticação (opcional).
        """
        self.headers = {"Authorization": f"token {token}"} if token else {}

    def search_repositories(self, query):
        """
        Busca repositórios no GitHub com base em uma query.
        :param query: Termo de busca.
        :return: Lista de repositórios.
        """
        url = f"{self.BASE_URL}/search/repositories"
        params = {"q": query}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            response.raise_for_status()

    def get_issues(self, owner, repo):
        """
        Obtém issues de um repositório específico.
        :param owner: Dono do repositório.
        :param repo: Nome do repositório.
        :return: Lista de issues.
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

# Buscar perguntas relacionadas a Flask
questions = StackExchangeAPI.search_questions("Flask API", tags=["python", "flask"])
for question in questions:
    print(f"{question['title']} - {question['link']}")

# Inicializar o cliente GitHub (adicione seu token, se necessário)
github_client = GitHubAPI(token="seu_token_aqui")

# Buscar repositórios relacionados a Flask
repos = github_client.search_repositories("Flask API")
for repo in repos:
    print(f"{repo['name']} - {repo['html_url']}")

# Obter issues de um repositório específico
issues = github_client.get_issues("pallets", "flask")
for issue in issues:
    print(f"{issue['title']} - {issue['html_url']}")