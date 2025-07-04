import requests
import json
import functools
import tkinter as tk
from tkinter import ttk

@functools.cache
def get_all_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon?limit=2000"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

@functools.cache
def get_all_pokemon_gen():
    url = "https://pokeapi.co/api/v2/generation/1/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    
@functools.cache
def get_all_pokemon_type():
    url = "https://pokeapi.co/api/v2/type/fire/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
#AllPokemon = get_all_pokemon()

#print(AllPokemon["results"][151])

#with open('AllPokemon.json', 'w') as file:
#    file.write(json.dumps(AllPokemon, indent = 4))

#with open('AllPokemon.json', 'r') as file:
    AllPokemon = file.read()
    AllPokemondict = json.loads(AllPokemon)

#print(AllPokemondict['results'][0]['name'])

#pokemonNames = []
#for pokemon in AllPokemondict['results']:
    pokemonNames.append(pokemon['name'])

#print(len(pokemonNames))
#print(pokemonNames)

#Gen1Poke = get_all_pokemon_gen()
#print(len(Gen1Poke["pokemon_species"]))
#for i in Gen1Poke["pokemon_species"]:
    #print(i["name"])

Type = get_all_pokemon_type()
print(json.dumps(Type["pokemon"], indent=4))

#root = tk.Tk()
#root.title("Pokedex")
#root.geometry("300x600")

#combo_box = ttk.Combobox(root, values = pokemonNames).grid(row=0,column=0)
#root.mainloop()
