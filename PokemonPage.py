import tkinter as tk
import requests
import json
import functools
from tkinter import font
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
        
        sprite = getImage()
        sprite2 = sprite.resize((400,400))
        self.sprite3 = ImageTk.PhotoImage(sprite2)

        #print(PokeInfo["species"]["url"])
        #print(PokeInfo["moves"])

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        info = BasicInfo(self,PokeInfo)
        info.grid(row = 0, column=0, sticky="nsew")

        Sprite = tk.Label(self, image=self.sprite3)
        Sprite.grid(row = 0, column=1, sticky="ne")

        text = tk.Label(self, text = "MOVES")
        text.grid(row = 1, column=0, sticky="nsew")

        text = tk.Label(self, text = "MISC INFO")
        text.grid(row = 1, column=1, sticky="nsew")


class BasicInfo(tk.Canvas):
    def __init__(self, parent, pokeinfo, *args, **kargs):
        tk.Canvas.__init__(self, parent, height= 400, *args, *kargs)
        self.parent = parent
        self.pokeinfo = pokeinfo
        
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1, uniform="row")
        self.grid_rowconfigure(1, weight = 1, uniform="row2")
        self.grid_rowconfigure(2, weight = 1, uniform="row")
        self.grid_rowconfigure(3, weight = 1, uniform="row2")
        self.grid_rowconfigure(4, weight = 1, uniform="row")
        self.grid_rowconfigure(5, weight = 1, uniform="row2")
        self.grid_rowconfigure(6, weight = 1, uniform="row")
        self.grid_rowconfigure(7, weight = 1, uniform="row2")

        DexNumber = pokeinfo["id"]
        def getGeneration():
            if DexNumber <= 151:
                return "GEN 1"
            elif 251 >= DexNumber > 151:
                return "GEN 2"
            elif 386 >= DexNumber > 251:
                return "GEN 3"
            elif 493 >= DexNumber > 386:
                return "GEN 4"
            elif 649 >= DexNumber > 493:
                return "GEN 5"
            elif 721 >= DexNumber > 649:
                return "GEN 6"
            elif 809 >= DexNumber > 721:
                return "GEN 7"
            elif 905 >= DexNumber > 809:
                return "GEN 8"
            elif 1025 >= DexNumber > 905:
                return "GEN 9"
            else:
                return "GEN XYZ"

        typestring = ""
        if len(self.pokeinfo["types"]) == 1:
            typestring += self.pokeinfo["types"][0]["type"]["name"]
        else:
            typestring = self.pokeinfo["types"][0]["type"]["name"].capitalize() + "/" + self.pokeinfo["types"][1]["type"]["name"].capitalize()
        
        CharInfo1 = f"{self.pokeinfo["name"].capitalize()}      National Dex #: {self.pokeinfo["id"]}      Type: {typestring}      {getGeneration()}"
        text = tk.Label(self, text = CharInfo1, padx = 30)
        text.config(font=("Bahnschrift SemiBold", 20))
        text.grid(row = 0, column=0, sticky = 'sw')

        line = lineSeperator(self, width=880, height=5)
        line.grid(row = 1, column=0, sticky = 'new')



        @functools.cache
        def get_species_link():
            response = requests.get(pokeinfo["species"]["url"])
            if response.status_code == 200:
                return response.json()
            else:
                print("error")
                return None
        specieslink = get_species_link()

        def get_evolution_info():
            response = requests.get(specieslink["evolution_chain"]["url"])
            if response.status_code == 200:
                return response.json()
            else:
                print("error")
                return None
        
        evolutioninfo = get_evolution_info()

        def getChain(info):
            if(len(info["evolves_to"])==0):
                return [info["species"]["name"]]
            if(len(info["evolves_to"])==2):
                return [info["species"]["name"]] + [getChain(info["evolves_to"][0]) + getChain(info["evolves_to"][1])]
            return [info["species"]["name"]] + getChain(info["evolves_to"][0])
        chain = getChain(evolutioninfo["chain"])

        chainstr = "Evolution Chain:  "
        if len(chain) == 1:
            chainstr += chain[0].capitalize()
        elif len(chain) > 1:
            for poke in chain:
                if(type(poke) == list):
                    chainstr += f"{poke[0].capitalize()}/{poke[1].capitalize()}"
                else:
                    chainstr += poke.capitalize() + "  "

        text2 = tk.Label(self, text = chainstr, padx = 30)
        text2.grid(row = 2, column=0, sticky = 'sw')
        text2.config(font=("Bahnschrift SemiBold", 15))

        line2 = lineSeperator(self, width=880, height=5)
        line2.grid(row = 3, column=0, sticky = 'new')



        abilitystring = ""
        for ability in pokeinfo["abilities"]:
            if ability["is_hidden"]:
                abilitystring += "Hidden: "
            abilitystring += ability["ability"]["name"].capitalize()
            abilitystring += ", "

        text3 = tk.Label(self, text = f"Abilities: {abilitystring[:-2]}", padx = 30)
        text3.grid(row = 4, column=0, sticky = 'sw')
        text3.config(font=("Bahnschrift SemiBold", 15))

        line3 = lineSeperator(self, width=880, height=5)
        line3.grid(row = 5, column=0, sticky = 'new')



        individualstats = []
        stattotal = 0
        for stat in pokeinfo["stats"]:
            stattotal+=int(stat["base_stat"])
            individualstats.append(stat["base_stat"])
        statstring = f"Stat Total: {stattotal}      HP: {individualstats[0]},  ATK: {individualstats[1]},  DEF: {individualstats[2]},  SpATK: {individualstats[3]},  SpDEF: {individualstats[4]},  SPD: {individualstats[5]}"

        text4 = tk.Label(self, text = statstring, padx = 30)
        text4.grid(row = 6, column=0, sticky = 'sw')
        text4.config(font=("Bahnschrift SemiBold", 15))

        line4 = lineSeperator(self, width=880, height=5)
        line4.grid(row = 7, column=0, sticky = 'new')


class lineSeperator(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.create_line(25, 3, 855, 3, fill="red", width=5)


if __name__ == "__main__":
    print()