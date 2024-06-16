# Pokédex por Tipo

Este é um aplicativo de Pokédex simples criado com Python e PyQt5, que permite aos usuários visualizar informações detalhadas sobre diferentes Pokémons. O aplicativo obtém dados da [PokeAPI](https://pokeapi.co/) e exibe uma lista de Pokémons filtrada por tipo.

## Funcionalidades

- Exibir uma lista de Pokémons com base no tipo selecionado.
- Mostrar detalhes sobre um Pokémon específico, incluindo habilidades, tipos, altura, peso e estatísticas.
- Exibir a imagem do Pokémon selecionado.

## Capturas de Tela

![pokedex](https://github.com/Brendo-will/Pokedex/assets/116374076/a6ad40f1-28e1-4566-b82d-ac78f26744fb)


## Requisitos

- Python 3.x
- PyQt5
- requests

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/Brendo-will/Pokedex
    cd Pokedex
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/Mac
    venv\Scripts\activate  # Para Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Execute o aplicativo:
    ```bash
    python pokedex.py
    ```

2. O aplicativo será iniciado e você poderá selecionar o tipo de Pokémon no menu suspenso para visualizar a lista de Pokémons desse tipo.

## Estrutura do Projeto

Pokedex/
│
├── pokedex.py 
├── requirements.txt 
├── README.md



## Agradecimentos

- [PokeAPI](https://pokeapi.co/) por fornecer a API para os dados dos Pokémons.
- [PyQt5](https://pypi.org/project/PyQt5/) por fornecer a biblioteca de interface gráfica.



