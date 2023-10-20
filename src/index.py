import requests
import asyncio
import os

# Chave da API do OMDB
api_key = "a15866fd"
class InsertMovies:
    def __init__(self):
        self.lista = []
        self.carregar_lista()
        
    def adicionar_lista(self, nova_lista):
        self.lista.append(nova_lista)
        self.salvar_lista()
    
    def salvar_lista(self):
        with open("filmes_favoritos.txt", "a") as file:
            for filme in self.lista:
                file.write(str(filme) + "\n")

    def carregar_lista(self):
        if os.path.exists("filmes_favoritos.txt"):
            with open("filmes_favoritos.txt", "r") as file:
                if os.stat("filmes_favoritos.txt").st_size != 0:
                    print("Filmes favoritos\n")
                    for line in file:
                        print(line)
                       
class cardMovies:
    def __init__(self, titulo, lancamento, classificacao,sinopse, diretor):
        self.titulo = titulo
        self.lancamento = lancamento
        self.classificacao = classificacao
        self.sinopse = sinopse
        self.diretor = diretor

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "lancamento": self.lancamento,
            "classificacao": self.classificacao,
            "sinopse": self.sinopse,
            "diretor": self.diretor
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["titulo"],
            data["lancamento"],
            data["classificacao"],
            data["sinopse"],
            data["diretor"]
        )
    
    @classmethod
    def from_string(cls, data_str):
        data = data_str.split(" | ")
        if len(data) == 5:
            return cls(data[0], data[1], data[2], data[3], data[4])
        return None   

    def __str__(self):
        return f'Filme: {self.titulo} - Ano de lançamento: {self.lancamento} - Classificação: {self.classificacao} - Sinopse: {self.sinopse} - Diretor: {self.diretor}'

async def search_movies(title: str):
    omdb_url = f'https://www.omdbapi.com/?t={title}&apikey={api_key}'

    try:
        response = requests.get(omdb_url)
        response.raise_for_status()  
        if response.status_code == 200:
            movie_data = response.json()
            print(f"\n-> Filme: {movie_data['Title']} - Ano de lançamento: {movie_data['Year']} - Classificação: {movie_data['Genre']} - Sinopse: {movie_data['Plot']} - Diretor: {movie_data['Director']}\n")
            print("\n1 - Deseja adicionar este filme aos favoritos ?")
            print("2 - Voltar")
            option = input("Escolha uma opção: ")
            if option == "1":
                print("Filme adicionado aos favoritos")
                return cardMovies(movie_data['Title'], movie_data['Year'], movie_data['Genre'], movie_data['Plot'], movie_data['Director'])
        
            elif option == "2":
                return
        else:
            print("Filme não encontrado")

    except requests.exceptions.HTTPError as err:
        print(f"Erro HTTP: {err}")

if __name__ == "__main__":
    AddMovies = InsertMovies()
    while True:
        print("\n1 - Buscar filmes")
        print("2 - Filmes favoritos")
        print("3 - Sair")
        option = input("Escolha uma opção: ")

        if option == "1":
            title = input("\nDigite o título do filme: ")
            title = title.replace(" ", "%20")
            Movies = asyncio.run(search_movies(title))
            if Movies:
                AddMovies.adicionar_lista(Movies)
        elif option == "2":
            AddMovies.carregar_lista()
            print("\n1 - Adicionar mais um filme aos favoritos")
            print("2 - Voltar")
            option = input("Escolha uma opção:")
            if option == "1":
                title = input("Digite o título do filme:")
                Movies = asyncio.run(search_movies(title))
                if Movies:
                    AddMovies.adicionar_lista(Movies)
        elif option == "3":
            break