import sys
import requests
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from functools import lru_cache

session = requests.Session()

@lru_cache(maxsize=None)
def get_pokemon_data(pokemon_name):
    """Buscar dados do Pokémon na PokeAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = session.get(url)
    if response.status_code == 200:
        data = response.json()
        species_url = data['species']['url']
        return {
            'name': data['name'],
            'abilities': [ability['ability']['name'] for ability in data['abilities']],
            'types': [ptype['type']['name'] for ptype in data['types']],
            'height': data['height'],
            'weight': data['weight'],
            'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
            'image_url': data['sprites']['front_default'],
        }
    else:
        return None

def fetch_all_pokemon():
    """Buscar uma lista de todos os nomes e tipos de Pokémon."""
    url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
    response = session.get(url)
    pokemon_list = []
    if response.status_code == 200:
        all_pokemon = response.json()['results']
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = executor.map(lambda p: get_pokemon_data(p['name']), all_pokemon)
            pokemon_list = [result for result in results if result]
    return pokemon_list

class PokedexWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background = QPixmap("/mnt/data/image.png")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

class PokemonApp(QWidget):
    def __init__(self, pokemon_list):
        super().__init__()
        self.pokemon_list = pokemon_list
        self.filtered_list = pokemon_list
        self.initUI()

    def initUI(self):
        self.setFixedSize(400, 600)
        main_layout = QVBoxLayout()
        self.pokedex_widget = PokedexWidget(self)
        
        inner_layout = QGridLayout()
        inner_layout.setContentsMargins(45, 100, 45, 150)

        self.typeCombo = QComboBox()
        self.typeCombo.addItem("Todos os Tipos")
        self.typeCombo.addItems(sorted(set(type for p in self.pokemon_list for type in p['types'])))
        self.typeCombo.currentIndexChanged.connect(self.filter_by_type)

        self.pokemonCombo = QComboBox()
        self.update_pokemon_combo()

        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel = QLabel("Selecione um Pokémon para ver seus detalhes.", self)
        self.resultLabel.setAlignment(Qt.AlignLeft)
        self.resultLabel.setWordWrap(True)

        inner_layout.addWidget(self.typeCombo, 0, 0, 1, 2)
        inner_layout.addWidget(self.pokemonCombo, 1, 0, 1, 2)
        inner_layout.addWidget(self.imageLabel, 2, 0, 1, 2)
        inner_layout.addWidget(self.resultLabel, 3, 0, 1, 2)

        main_layout.addWidget(self.pokedex_widget)
        self.pokedex_widget.setLayout(inner_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Pokédex por Tipo')
        self.show()

    def update_pokemon_combo(self):
        self.pokemonCombo.clear()
        self.pokemonCombo.addItems([p['name'].title() for p in self.filtered_list])
        self.pokemonCombo.currentIndexChanged.connect(self.display_pokemon_details)

    def filter_by_type(self):
        selected_type = self.typeCombo.currentText()
        if (selected_type == "Todos os Tipos") or (selected_type is None):
            self.filtered_list = self.pokemon_list
        else:
            self.filtered_list = [p for p in self.pokemon_list if selected_type in p['types']]
        self.update_pokemon_combo()

    def display_pokemon_details(self):
        selected_pokemon = self.pokemonCombo.currentText().lower()
        for p in self.filtered_list:
            if p['name'] == selected_pokemon:
                pixmap = QPixmap()
                pixmap.loadFromData(requests.get(p['image_url']).content)
                self.imageLabel.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                
                details = [
                    f"Nome: {p['name'].title()}",
                    f"Habilidades: {', '.join(p['abilities'])}",
                    f"Tipos: {', '.join(p['types'])}",
                    f"Altura: {p['height']} decímetros",
                    f"Peso: {p['weight']} hectogramas",
                    "Estatísticas:"
                ]
                stats = [f"  {stat}: {value:2}" for stat, value in p['stats'].items()]
                details.extend(stats)              

                self.resultLabel.setText("\n".join(details))
                break

def main():
    app = QApplication(sys.argv)
    pokemon_list = fetch_all_pokemon()  
    ex = PokemonApp(pokemon_list)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
