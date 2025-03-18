import requests
import json
import functools


def get_all_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon?limit=2000"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

AllPokemon = get_all_pokemon()

print(AllPokemon["results"][151])

with open('AllPokemon.json', 'w') as file:
    file.write(json.dumps(AllPokemon, indent = 4))