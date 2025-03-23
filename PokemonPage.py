import tkinter as tk
import requests
import json
import functools
from tkinter import font
from PIL import ImageTk, Image
from io import BytesIO

#Toplevel window that shows the selected pokemon's information
#Topwindow because its common to want to look up multiple pokemon to compare them
class PokemonPage(tk.Toplevel):
    #Name gets passed in initialization so that I can pull the information from the api
    def __init__(self, parent, pokename, *args, **kargs):
        tk.Toplevel.__init__(self, parent, *args, **kargs)

        #Setting window name in accordance to pokemon name as well as window size
        self.title(pokename.capitalize())
        self.pokename = pokename
        self.geometry("1280x720")
        self.minsize(1280,720)
        self.maxsize(1280,720)

        #Get the pokemon url via the name by finding it in the AllPokemon.json file which was made through the https://pokeapi.co/api/v2/pokemon?limit=2000 call
        #Realisticly I should probbaly pass the url along with the name when the search algorithm gets implemented because I will probably get that info then
        #That would probably be more efficient but I made this page first and wanted a easy out while I designed the pokemon page
        def getPokemonURL():
            with open('AllPokemon.json', 'r') as file:
                AllPokemon = file.read()
                AllPokemondict = json.loads(AllPokemon)
                for pokemon in AllPokemondict['results']:
                    if self.pokename == pokemon['name']:
                        return pokemon["url"]            
        url = getPokemonURL()

        #Get the respective pokemon info using the url
        @functools.cache
        def get_pokemon_info():
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print("error")
                return None
        PokeInfo = get_pokemon_info()
        
        #Get the pokemon picture url in the info pulled from the last call 
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
        #Not sure if needed if all the pictures in the api are the same size, but resize them to make sure
        sprite2 = sprite.resize((400,400))
        self.sprite3 = ImageTk.PhotoImage(sprite2)

        #The toplevel is split up into 4 sections: Basic Pokemon information, Pokemon Moves, Pokemon picture, and Misc Info
        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        #Basic Info
        info = BasicInfo(self,PokeInfo)
        info.grid(row = 0, column=0, sticky="nsew")

        #Picture
        Sprite = tk.Label(self, image=self.sprite3)
        Sprite.grid(row = 0, column=1, sticky="ne")

        #Moves
        #Made a border frame so i can easily see the frame where moves are shown
        borderframe = tk.Frame(self, highlightbackground="red", highlightcolor="red", highlightthickness=2)
        borderframe.grid(row = 1, column=0, sticky="nsew", padx = 5, pady = 5)
        borderframe.grid_columnconfigure(0, weight = 1)
        borderframe.grid_rowconfigure(0, weight = 1)
        #Actual moves scrollable
        text = moves(borderframe, PokeInfo)
        text.grid(row= 0, column = 0, sticky="nsew")
        
        #Misc info
        #Again, could and should make a frame object, but the point is still there
        text = tk.Frame(self, highlightbackground="red", highlightcolor="red", highlightthickness=2)
        text.grid(row = 1, column=1, sticky="nsew", padx = 5, pady = 5)
        text.rowconfigure(0, weight=1)
        text.rowconfigure(1, weight=1)
        text.columnconfigure(0, weight=1)

        text1 = tk.Label(text,font=("Bahnschrift SemiBold", 10), text= f"Standard Height: {PokeInfo["height"]/10} Meters")
        text1.grid(row = 0)
        text2 = tk.Label(text,font=("Bahnschrift SemiBold", 10), text = f"Standard Weight: {PokeInfo["weight"]/10} Kilograms")
        text2.grid(row = 1)


class BasicInfo(tk.Canvas):
    def __init__(self, parent, pokeinfo, *args, **kargs):
        tk.Canvas.__init__(self, parent, height= 400, *args, *kargs)
        self.parent = parent
        self.pokeinfo = pokeinfo
        
        #Rows are the text information, row2's are red seperator lines
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1, uniform="row")
        self.grid_rowconfigure(1, weight = 1, uniform="row2")
        self.grid_rowconfigure(2, weight = 1, uniform="row")
        self.grid_rowconfigure(3, weight = 1, uniform="row2")
        self.grid_rowconfigure(4, weight = 1, uniform="row")
        self.grid_rowconfigure(5, weight = 1, uniform="row2")
        self.grid_rowconfigure(6, weight = 1, uniform="row")
        self.grid_rowconfigure(7, weight = 1, uniform="row2")

        #Get generation number based on national dex number
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

        #Get and format pokemon types from the info pulled from api and passed to BasicInfo
        typestring = ""
        if len(self.pokeinfo["types"]) == 1:
            typestring += self.pokeinfo["types"][0]["type"]["name"].capitalize()
        else:
            typestring = self.pokeinfo["types"][0]["type"]["name"].capitalize() + "/" + self.pokeinfo["types"][1]["type"]["name"].capitalize()
        
        #Format name, Dex number, type and generation string
        CharInfo1 = f"{self.pokeinfo["name"].capitalize()}      National Dex #: {self.pokeinfo["id"]}      Type: {typestring}      {getGeneration()}"
        
        #Write it out, give it a better font, and biggest size for a "title" like look, stiky it to the bottom left close to the line seperator
        text = tk.Label(self, text = CharInfo1, padx = 30)
        text.config(font=("Bahnschrift SemiBold", 20))
        text.grid(row = 0, column=0, sticky = 'sw')
        #Line seperator, sticky it to the top close to the text
        line = lineSeperator(self, width=880, height=5)
        line.grid(row = 1, column=0, sticky = 'new')

        #Getting evolution info is a bit more complicated bacuse it isnt directly in the pokemon info
        #I need to pull the species info url from the pokemon info and then pull the evolution chain url from the species info
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

        #Getting the evolution chain
        #Right now uses a small recursive function to get the chain becasue the next pokemon in the evolution is inside the previous pokemon info here
        #This works only for pokemon where the chain is 1 / 1->2 / 1->2->3
        #This doesnt work and needs to be updated for pokemon like wurmple, eeevee, etc which have seperate chains
        def getChain(info):
            if(len(info["evolves_to"])==0):
                return [info["species"]["name"]]
            if(len(info["evolves_to"])==2):
                return [info["species"]["name"]] + [getChain(info["evolves_to"][0]) + getChain(info["evolves_to"][1])]
            return [info["species"]["name"]] + getChain(info["evolves_to"][0])
        chain = getChain(evolutioninfo["chain"])

        #Setup the string with the evolution chain
        chainstr = "Evolution Chain:  "
        if len(chain) == 1:
            chainstr += chain[0].capitalize()
        elif len(chain) > 1:
            for poke in chain:
                if(type(poke) == list):
                    chainstr += f"{poke[0].capitalize()}/{poke[1].capitalize()}"
                else:
                    chainstr += poke.capitalize() + "  "

        #Write it out, give it a better font, and give it a smaller font than the "title", sticky it to the bottom left close to the line seperator
        text2 = tk.Label(self, text = chainstr, padx = 30)
        text2.grid(row = 2, column=0, sticky = 'sw')
        text2.config(font=("Bahnschrift SemiBold", 15))
        #Line seperator, sticky it to the top close to the text
        line2 = lineSeperator(self, width=880, height=5)
        line2.grid(row = 3, column=0, sticky = 'new')

        #Format the ability string with the info in pokeinfo
        abilitystring = ""
        for ability in pokeinfo["abilities"]:
            if ability["is_hidden"]:
                abilitystring += "Hidden: "
            abilitystring += ability["ability"]["name"].capitalize()
            abilitystring += ", "

        #Write it out, give it a better font, and give it a smaller font than the "title", sticky it to the bottom left close to the line seperator
        text3 = tk.Label(self, text = f"Abilities: {abilitystring[:-2]}", padx = 30)
        text3.grid(row = 4, column=0, sticky = 'sw')
        text3.config(font=("Bahnschrift SemiBold", 15))
        #Line seperator, sticky it to the top close to the text
        line3 = lineSeperator(self, width=880, height=5)
        line3.grid(row = 5, column=0, sticky = 'new')


        #Get the individual stats and the total of all the stats from pokeinfo, the format the string
        individualstats = []
        stattotal = 0
        for stat in pokeinfo["stats"]:
            stattotal+=int(stat["base_stat"])
            individualstats.append(stat["base_stat"])
        statstring = f"Stat Total: {stattotal}      HP: {individualstats[0]},  ATK: {individualstats[1]},  DEF: {individualstats[2]},  SpATK: {individualstats[3]},  SpDEF: {individualstats[4]},  SPD: {individualstats[5]}"
        #Write it out, give it a better font, and give it a smaller font than the "title", sticky it to the bottom left close to the line seperator
        text4 = tk.Label(self, text = statstring, padx = 30)
        text4.grid(row = 6, column=0, sticky = 'sw')
        text4.config(font=("Bahnschrift SemiBold", 15))
        #Line seperator, sticky it to the top close to the text
        line4 = lineSeperator(self, width=880, height=5)
        line4.grid(row = 7, column=0, sticky = 'new')

#Line seperator object, literally just a red line to be put under text to act as a section seperator of sorts
class lineSeperator(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.create_line(25, 3, 855, 3, fill="red", width=5)

class moves(tk.Frame):
    def __init__(self, parent, pokeinfo, *args, **kargs):
        tk.Frame.__init__(self, parent, *args, *kargs)
        self.pokeinfo = pokeinfo
        self.parent = parent

        #Make a canvas to house Scrollbar and Scrollable contents
        self.canvas = tk.Canvas(self, height = 280, width = 820)
        self.canvas.grid(row=0, column=0, sticky="nsew",padx=10, pady=10)
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)

        #Make tk scrollbar
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row= 0, column=1, sticky="ns")

        #Configure scrollbar to stay in position based on where its scrolled
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        #Frame that houses all the moves
        self.scrollable = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.scrollable, anchor="nw")

        #Move Objects
        self.count = 0
        for row in self.pokeinfo["moves"]:
            tk.Label(self.scrollable, text=row["move"]["name"].capitalize(),font=("Bahnschrift SemiBold", 10)).grid(row=self.count//5,column=self.count%5,pady=10,padx = 35, sticky = "we")
            self.count+=1

        #Keeps the scrollable portion in the spot that its left in
        def update_scroll(event):
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scrollable.bind("<Configure>", update_scroll)


if __name__ == "__main__":
    print()