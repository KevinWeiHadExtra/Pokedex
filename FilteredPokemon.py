import tkinter as tk
import requests
import json
import functools
from PokemonPage import PokemonPage

class FilteredPokemon(tk.Toplevel):
    def __init__(self, parent, filterlist, *args, **kargs):
        tk.Toplevel.__init__(self, parent, *args, **kargs)

        self.title("Filtered Pokemon")
        self.filterlist = filterlist
        self.geometry("1280x720")
        self.minsize(1280,720)
        self.maxsize(1280,720)

        self.canvas = tk.Canvas(self, height = 700, width = 1258, highlightbackground="red", highlightcolor="red", highlightthickness=3)
        self.canvas.grid(row=0, column=0, sticky="nw")

        #Make tk scrollbar
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row= 0, column=1, sticky="nes")
        
        #Configure scrollbar to stay in position based on where its scrolled
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        #Frame that houses all the SearchResult objects
        self.scrollable = tk.Frame(self.canvas)
        self.scrollable.grid_columnconfigure(0, weight=1, uniform="1")
        self.scrollable.grid_columnconfigure(0, weight=1, uniform="1")
        self.canvas.create_window((0,0), window=self.scrollable, anchor="nw")

        #make all the CharLayout objects for all the entries in the GENSHINCHARACTER table
        self.count = 0
        for row in self.filterlist:
            SearchResult(self.scrollable, row).grid(row=self.count//2,column=self.count%2, pady=20, padx = 55, sticky="nsew")
            self.count+=1

        #Keeps the scrollable portion in the spot that its left in
        def update_scroll(event):
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scrollable.bind("<Configure>", update_scroll)

class SearchResult(tk.Frame):
    def __init__(self, parent, pokemonname):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.pokemoname = pokemonname
        #These are current divied up loosely because I didnt want to make six calls on the search page to get more information on the pokemon, but it can and probably will be added later.
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        #Name
        Name = tk.Label(self, text = self.pokemoname.capitalize(), font=("Bahnschrift SemiBold", 15), width= 40, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        Name.grid(row = 0, column = 0, sticky="nsew", padx=5, pady=5)

        #Button that opens up the pokemons toplevel page
        Open = tk.Button(self, text = "Go", font=("Bahnschrift SemiBold", 10), width = 5, command = self.PokemonEntry)
        Open.grid(row = 0, column = 1, sticky="we", padx=5, pady=5)

    #Open the toplevel page
    def PokemonEntry(self):
        PokePage = PokemonPage(self, self.pokemoname)