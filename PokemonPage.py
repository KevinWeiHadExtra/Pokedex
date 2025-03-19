import tkinter as tk
import requests
import json
import functools

class PokemonPage(tk.Toplevel):
    def __init__(self, parent, pokename, *args, **kargs):
        tk.Toplevel.__init__(self, parent, *args, **kargs)

        self.title(pokename.capitalize())
        self.pokename = pokename
        self.geometry("1280x720")
        self.minsize(1280,720)
        self.maxsize(1280,720)

        def getPokemonURL():
            with open('AllPokemon.json', 'r') as file:
                AllPokemon = file.read()
                AllPokemondict = json.loads(AllPokemon)
                for pokemon in AllPokemondict['results']:
                    if self.pokename == pokemon['name']:
                        return pokemon["url"]
                    
        @functools.cache
        def get_pokemon_info():
            response = requests.get(getPokemonURL())
            if response.status_code == 200:
                return response.json()
            else:
                return None

        pokeurl = getPokemonURL()
        print(pokeurl)

if __name__ == "__main__":
    print()