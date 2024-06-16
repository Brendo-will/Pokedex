import sys
import requests
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from concurrent.futures import ThreadPoolExecutor

def get_pokemon_data(pokemon_name):
    """Fetch Pokemon data from the PokeAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'name': data['name'],
            'abilities': [ability['ability']['name'] for ability in data['abilities']],
            'types': [ptype['type']['name'] for ptype in data['types']],
            'height': data['height'],
            'weight': data['weight'],
            'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
            'image_url': data['sprites']['front_default']
        }
    else:
        return None

def fetch_all_pokemon():
    """Fetch a list of all Pokémon names and types."""
    url = "https://pokeapi.co/api/v2/pokemon?limit=150"
    response = requests.get(url)
    pokemon_list = []
    if response.status_code == 200:
        all_pokemon = response.json()['results']
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(lambda p: get_pokemon_data(p['name']), all_pokemon)
            pokemon_list = [result for result in results if result]
    return pokemon_list

class PokemonApp(QWidget):
    def __init__(self, pokemon_list):
        super().__init__()
        self.pokemon_list = pokemon_list
        self.filtered_list = pokemon_list
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        bottom_layout = QVBoxLayout()

        self.typeCombo = QComboBox()
        self.typeCombo.addItem("All Types")
        self.typeCombo.addItems(sorted(set(type for p in self.pokemon_list for type in p['types'])))
        self.typeCombo.currentIndexChanged.connect(self.filter_by_type)

        self.pokemonCombo = QComboBox()
        self.update_pokemon_combo()

        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel = QLabel("Select a Pokémon to see its details.", self)
        self.resultLabel.setAlignment(Qt.AlignLeft)

        top_layout.addWidget(self.typeCombo)
        top_layout.addWidget(self.pokemonCombo)
        bottom_layout.addWidget(self.imageLabel)
        bottom_layout.addWidget(self.resultLabel)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Pokédex by Type')
        self.setFixedSize(600, 400) 
        self.show()

    def update_pokemon_combo(self):
        self.pokemonCombo.clear()
        self.pokemonCombo.addItems([p['name'].title() for p in self.filtered_list])
        self.pokemonCombo.currentIndexChanged.connect(self.display_pokemon_details)

    def filter_by_type(self):
        selected_type = self.typeCombo.currentText()
        if selected_type == "All Types":
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
                    f"Name: {p['name'].title()}",
                    f"Abilities: {', '.join(p['abilities'])}",
                    f"Types: {', '.join(p['types'])}",
                    f"Height: {p['height']} decimetres",
                    f"Weight: {p['weight']} hectograms",
                    "Stats:"
                ]
                stats = [f"  {stat}: {value:2}" for stat, value in p['stats'].items()]
                details.extend(stats)
                self.resultLabel.setText("\n".join(details))
                break

def main():
    app = QApplication(sys.argv)
    pokemon_list = fetch_all_pokemon()  # Fetch all Pokémon when the app starts
    ex = PokemonApp(pokemon_list)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
