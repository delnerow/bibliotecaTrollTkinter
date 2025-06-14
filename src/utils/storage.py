import json

from src.models import Livro

DATA_FILE = 'data.json'
def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            catalogo = []
            if data and 'livros' in data:
                for t in data['livros']:
                    catalogo.append(Livro.from_dict(t))
            return catalogo
    except FileNotFoundError:
        return []

def save_data(catalogo):
    data = {
        'livros': [t.to_dict() for t in catalogo]
    }
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)