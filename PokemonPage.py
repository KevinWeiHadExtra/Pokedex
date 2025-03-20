import tkinter as tk
import requests
import json
import functools
from PIL import ImageTk, Image
from io import BytesIO

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
                    
        url = getPokemonURL()

        @functools.cache
        def get_pokemon_info():
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print("error")
                return None
        
        PokeInfo = get_pokemon_info()

        DexNumber = PokeInfo["id"]
        def getGeneration():
            if DexNumber <= 151:
                return "Generation 1"
            elif 251 >= DexNumber > 151:
                return "Generation 2"
            elif 386 >= DexNumber > 251:
                return "Generation 3"
            elif 493 >= DexNumber > 386:
                return "Generation 4"
            elif 649 >= DexNumber > 493:
                return "Generation 5"
            elif 721 >= DexNumber > 649:
                return "Generation 6"
            elif 809 >= DexNumber > 721:
                return "Generation 7"
            elif 905 >= DexNumber > 809:
                return "Generation 8"
            elif 1025 >= DexNumber > 905:
                return "Generation 9"
            else:
                return "Generation XYZ"
        
        imageURL = PokeInfo["sprites"]["other"]["official-artwork"]["front_default"]
        def getImage():
            response = requests.get(imageURL)
            if response.status_code == 200:
                print("Got")
                image = Image.open(BytesIO(response.content))
                return image
            else:
                print("error")
                return None
        
        image = getImage()
        #image.show()

        print(PokeInfo["id"])
        print(PokeInfo["name"])
        print(getGeneration())
        print(PokeInfo["types"])
        print(PokeInfo["abilities"])
        print(PokeInfo["species"])
        print(PokeInfo["stats"])
        #print(PokeInfo["moves"])

        



if __name__ == "__main__":
    print()