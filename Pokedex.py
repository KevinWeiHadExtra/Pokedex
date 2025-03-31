import tkinter as tk
import requests
import json
from PIL import ImageTk, Image
from PokemonPage import PokemonPage
from FilteredPokemon import FilteredPokemon
from difflib import SequenceMatcher

#Main Tk objects
class Pokedex(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #Setting window name and size
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title("Pokedex")
        self.geometry("1280x720")
        self.minsize(1280,720)
        self.maxsize(1280,720)

        #Frame that will hold the 3 frames that will be switched betwee, start, search, advancedsearch
        rootwindow = tk.Frame(self)
        rootwindow.grid(row=0, column=0, sticky="nsew")
        rootwindow.grid_rowconfigure(0, weight=1)
        rootwindow.grid_columnconfigure(0, weight=1)

        #Make all the pages
        self.pages = {}
        for page in (Start, Search, AdvancedSearch):
            pagename = page.__name__
            frame = page(parent=rootwindow, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[pagename] = frame
        
        #Set the starting frame to Start
        self.topPage("Start")
    
    #raise the selected frame
    def topPage(self, pagename):
        frame = self.pages[pagename]
        frame.tkraise()

    def passSearch(self, name):
        self.pages["Search"].update_search_entry(name)

    #def update(self):
    #    self.update()

#Starting frame
class Start(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #Start Frame is first split into 4, Rows, all in one column
        #First and last row are set for and "aesthetic" uniform header and footer
        #Second and third are set to the Pokedex text logo and search funtions respectfully
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1, uniform="topdown")
        self.rowconfigure(1, weight = 1, uniform="center")
        self.rowconfigure(2, weight = 1, uniform="center")
        self.rowconfigure(3, weight = 1, uniform="topdown")

        #Red Header
        Header = tk.Frame(self, bg = "red", height=5)
        Header.grid(row=0, column=0, sticky="nsew")
        Header.grid_rowconfigure(0, weight=1)
        
        #Logo
        self.PokedexPic = ImageTk.PhotoImage(Image.open("PokedexLogo.png"))
        Logo = tk.Label(self, image=self.PokedexPic)
        Logo.grid(row = 1, column=0, sticky="nsew")

        #The Search section is then split off in its own frame
        #The bar takes up the first row and 2 columns
        #Then the second row has the search button and advanced search button in their own column, stickyed towards the center
        #This could and probably should be its own class
        Searchbar = tk.Frame(self)
        Searchbar.grid(row= 2, column=0, sticky="nsew")
        Searchbar.grid_rowconfigure(0, weight=1)
        Searchbar.grid_rowconfigure(1, weight=1)
        Searchbar.grid_columnconfigure(0, weight=1)
        Searchbar.grid_columnconfigure(1, weight=1)

        self.usersearch = tk.StringVar()
        #Searchbar
        Bar = tk.Entry(Searchbar, width=50, font=("Bahnschrift SemiBold", 15), textvariable=self.usersearch)
        Bar.grid(row=0,column=0, columnspan=2)

        #Search Button
        SearchButton = tk.Button(Searchbar, text = "Search", font=("Bahnschrift SemiBold", 10), width=20, command = self.searchbutton)
        SearchButton.grid(row=1, column=0, sticky="ne", padx = 10)

        #Advanced Search button
        AdvancedSearchButton = tk.Button(Searchbar, text = "Advanced Search", font=("Bahnschrift SemiBold", 10), width=20, command=self.filterbutton)
        AdvancedSearchButton.grid(row = 1, column=1, sticky="nw", padx = 10)
        
        #Red Footer
        Footer = tk.Frame(self, bg = "red", height=5)
        Footer.grid(row=3, column=0, sticky="nsew")
        Footer.grid_rowconfigure(0, weight=1)
    
    def searchbutton(self):
        self.controller.topPage("Search")
        self.controller.passSearch(self.usersearch.get())

    def filterbutton(self):
        self.controller.topPage("AdvancedSearch")


    #Test function currently in so I have easy access to the Pokemon page, bypassing the search function right now
    def PokemonEntry(self, str = "goodra"):
        PokePage = PokemonPage(self, str)
        

#Frame that shows the results of the search algorithm
class Search(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.searchentry = tk.StringVar()

        #Split into 3 "sections"
        #Header and footer, just a red bar
        #Actual header in a sense where there is a button to the start page and the advanced search page, along with text saying this is the search page
        #The actual Search section
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        #Header Red bar
        Header = tk.Frame(self, bg = "red", height = 10 )
        Header.grid(row = 0, column=0,sticky="nsew", columnspan=3)

        #Button back to start page
        Button = tk.Button(self, text = "<-- Start", font=("Bahnschrift SemiBold", 10), width = 20, command = lambda:self.controller.topPage("Start"))
        Button.grid(row = 1, column = 0, sticky="nw", padx=10, pady=10)

        #Search text
        PageName = tk.Label(self, text = "Search", font=("Bahnschrift SemiBold", 15))
        PageName.grid(row = 1, column = 1, sticky="we", padx=10, pady=10)

        #button to advanced search
        Button = tk.Button(self, text = "Advanced Search -->", font=("Bahnschrift SemiBold", 10), width = 20, command = lambda:self.controller.topPage("AdvancedSearch"))
        Button.grid(row = 1, column = 2, sticky="ne", padx=10, pady=10)

        #Initial frame to house everything in the correct grid spot on the search page frame and so I can give it a red border to house the section
        borderframe = tk.Frame(self, highlightbackground="red", highlightcolor="red", highlightthickness=2)
        borderframe.grid(row = 2, column=0, columnspan=3, sticky="nsew", padx = 5, pady = 5)
        borderframe.grid_columnconfigure(0, weight = 1)
        borderframe.grid_rowconfigure(0, weight = 1)
        
        #The searchframe object that houses the pages searchbar, button, and results
        self.searchframe = SearchFrame(borderframe, self.searchentry.get())
        self.searchframe.grid(row = 0, column = 0, sticky="nsew")

        #Footer Red bar
        Footer = tk.Frame(self, bg = "red", height = 10 )
        Footer.grid(row = 3, column=0,sticky="nsew", columnspan=3)
    
    #Function that takes the new user entry in the search bar and remakes the searchframe object with the new results.
    #This is needed because since the start, search, and advanced search pages are all technically on top of each other they are all made at runtime
    #So in order to change them according to new user entries they need to be remade
    #This is called in the master Pokedex class in the passsearch funtion. And the passsearch function is called via the start page when trasitioning to the search page with the user entry in the start page
    #Updating in the start page will be handled in the SearchFrame Frame
    def update_search_entry(self, entry):
        self.searchentry.set(entry)
        self.searchframe.destroy()
        self.searchframe = SearchFrame(self.searchframe.master, self.searchentry.get())
        self.searchframe.grid(row = 0, column = 0, sticky="nsew")

#Object that contains the actual search funtions in the search page
class SearchFrame(tk.Frame):
    def __init__(self, parent, searchentry):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.searchentry = tk.StringVar()
        self.searchentry.set(searchentry)
        
        #This frame is seperated into 3 sections
        #The searchbar and button
        #The redline seperator
        #The search results
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        #Searchbar and button
        Bar = tk.Entry(self, width=85, font=("Bahnschrift SemiBold", 15), textvariable=self.searchentry)
        Bar.grid(row=0,column=0, padx = 10, pady = 10)

        Button = tk.Button(self, text = "Search", font=("Bahnschrift SemiBold", 10), width = 10, command=self.updatesearch)
        Button.grid(row = 0, column = 1, sticky="we", padx=10, pady=10)

        #Redline seperator
        Seperator = tk.Frame(self, bg = "red", height = 2 )
        Seperator.grid(row = 1, column=0, sticky="nsew", columnspan=2, padx = 5, pady = 5)
        
        #Frame that houses the results
        #Has 2 colums and 3 rows to house 6 widgets max
        self.borderframe = tk.Frame(self)
        self.borderframe.grid(row = 2, column=0, columnspan=2, sticky="nsew", padx = 5, pady = 5)
        self.borderframe.grid_columnconfigure(0, weight = 1)
        self.borderframe.grid_columnconfigure(1, weight = 1)
        self.borderframe.grid_rowconfigure(0, weight = 1)
        self.borderframe.grid_rowconfigure(1, weight = 1)
        self.borderframe.grid_rowconfigure(2, weight = 1)
        
        #Get 6 results, get6results is the function that returns the six pokemon names most similar to the users input according to SequenceMatcher
        self.searchresults = self.get6results(self.searchentry.get())
        
        #Make the 6 widgets with each of the pokemon in the right rows and columns
        count = 0
        self.results = []
        for i in self.searchresults:
            box = SearchResult(self.borderframe, i)
            box.grid(row=count//2,column=count%2,padx=20,pady=10, sticky = "nsew")
            box.grid_propagate(False)
            self.results.append(box)
            count+=1
    
    #This is the updatesearch function that is used inside the search page
    #Instead of the one used from the start page that remakes the Searchframe widget obeject, this function remakes the Searchresult widgets
    #Ideally both functions would probably behave the same way, but this is how I built it while learning
    def updatesearch(self):
        #Get the new user entry
        self.searchresults = self.get6results(self.searchentry.get())
        counter = 0
        #These conditions are made to check in case there was a situation wehre someone searched when there was no input. These are kind of important becasue the search from the start page also augments these variables.
        #This is probably easier if I made the start and search page search functions funtion the same way but alas

        #If There were prior Searchresult wigets made
        if len(self.results) > 0 :
            #First check if the new input is empty, if it is, destroy all the widgets and dont replace them because there was no input
            if len(self.searchresults) == 0:
                for i in self.results:
                    i.destroy()
            #Otherwise if there was an input, destroy and replace the old SearchResult widgets with new ones
            else:
                newsearches = []
                for i,y in zip(self.results,self.searchresults):
                    i.destroy()
                    if y != "":
                        box = SearchResult(self.borderframe, y)
                        box.grid(row=counter//2,column=counter%2,padx=20,pady=10, sticky = "nsew")
                        box.grid_propagate(False)
                        newsearches.append(box)
                        counter+=1
                self.results = newsearches
        #If there werent prior searches made, ie all prior searches were empty and there are no prexisting widgets
        else:
            #Just make 6 new widgets according to the 6 results
            count = 0
            for i in self.searchresults:
                box = SearchResult(self.borderframe, i)
                box.grid(row=count//2,column=count%2,padx=20,pady=10, sticky = "nsew")
                box.grid_propagate(False)
                self.results.append(box)
                count+=1

    #The search funtion
    def get6results(self, searched):
        justNames = []
        pokemonNames = {}
        #If there was no user input, do nothing and return an empty list
        if searched != "":
            #Open up the file that contains a list of all pokemon names
            with open('AllPokemon.json', 'r') as file:
                AllPokemon = file.read()
                AllPokemondict = json.loads(AllPokemon)
            counter = 0
            #Iterate through the list
            for pokemon in AllPokemondict['results']:
                #Use sequence matcher to compare the users input agains all the pokemon names
                similarity = SequenceMatcher(None, searched.casefold(), pokemon['name'].casefold()).ratio()
                #Get 6 results and put them in just becasue I only want the top 6 most similar results
                if counter < 6:
                    #Put them into a dictionary as key:Name and Value:Similarity
                    pokemonNames[pokemon['name']] = similarity
                    #Sort the dintionary by lowest to highest similarity
                    sorted_dict = sorted(pokemonNames.items(), key=lambda item: item[1])
                    #Assign the new dict
                    pokemonNames = dict(sorted_dict)
                    counter+=1
                #When there are 6 results we dont want to add any more. We just want to replace lower similarities with higer similarities
                elif counter == 6:
                    #Since the dinct is ordered with the lowest similarity value in front we grab the first key
                    first = next(iter(pokemonNames))
                    #If the first keys value is less than the new pokemons similarity we add the new pokemon into the dict and remove the old one
                    if pokemonNames[first] < similarity:
                        pokemonNames[pokemon['name']] = similarity
                        pokemonNames.pop(first)
                        #Then resort so that the lowest value is once again at the front
                        sorted_dict = sorted(pokemonNames.items(), key=lambda item: item[1])
                        pokemonNames = dict(sorted_dict)
            #Get a list of the 6 results keys becasue those are the names
            justNames = list(pokemonNames.keys())
            #Reverse the list so that it is now most similar to least similar from those 6
            justNames.reverse()
        return justNames

#The searchreusult object, there will be 6 of these for 6 results in the SearchFrame widget
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
        

#Filter search Frame for getting a list of  results aligning with selected filters
class AdvancedSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        Header = tk.Frame(self, bg = "red", height = 10 )
        Header.grid(row = 0, column=0,sticky="nsew", columnspan=3)

        Button = tk.Button(self, text = "<-- Search", font=("Bahnschrift SemiBold", 10), width = 20, command = lambda:self.controller.topPage("Search"))
        Button.grid(row = 1, column = 0, sticky="nw", padx=10, pady=10)

        PageName = tk.Label(self, text = "Advanced Search", font=("Bahnschrift SemiBold", 15))
        PageName.grid(row = 1, column = 1, sticky="we", padx=10, pady=10)

        Button = tk.Button(self, text = "Start -->", font=("Bahnschrift SemiBold", 10), width = 20, command = lambda:self.controller.topPage("Start"))
        Button.grid(row = 1, column = 2, sticky="ne", padx=10, pady=10)

        borderframe = tk.Frame(self, highlightbackground="red", highlightcolor="red", highlightthickness=2)
        borderframe.grid(row = 2, column=0, columnspan=3, sticky="nsew", padx = 5, pady = 5)
        borderframe.grid_columnconfigure(0, weight = 1, uniform="col")
        borderframe.grid_columnconfigure(1, weight = 1, uniform="col")
        borderframe.grid_rowconfigure(0, weight = 1)
        borderframe.grid_rowconfigure(1, weight = 1)

        self.Generations = GenCheck(borderframe)
        self.Generations.grid(row = 0, column=0, sticky="nsew", padx = 5, pady = 5, rowspan=2)

        self.Type = TypeCheck(borderframe)
        self.Type.grid(row=0,column=1, sticky="nsew", padx = 5, pady = 5)

        FilterButton = tk.Button(borderframe, text = "Filter Search", font=("Bahnschrift SemiBold", 15), width = 20, command=self.getFilters)
        FilterButton.grid(row = 1, column=1, padx = 5, pady = 5)

        Footer = tk.Frame(self, bg = "red", height = 10 )
        Footer.grid(row = 3, column=0,sticky="nsew", columnspan=3)

    def getFilters(self):
        genList = self.Generations.getGen()
        type = self.Type.getType()
        genPokemon = []
        typePokemon = []
        for gen, yes in enumerate(genList):
            if yes == 1:
                url = f"https://pokeapi.co/api/v2/generation/{gen+1}/"
                response = requests.get(url)
                data = response.json()
                for i in data["pokemon_species"]:
                    genPokemon.append(i["name"])
        
        typeurl = "https://pokeapi.co/api/v2/type/" + type + "/"
        typeresponse = requests.get(typeurl)
        typedata = typeresponse.json()
        for x in typedata["pokemon"]:
            typePokemon.append(x["pokemon"]["name"])
        
        filtered = set(typePokemon).intersection(set(genPokemon))
        filteredlist = list(filtered)
        filteredlist.sort()
        ResultsPage = FilteredPokemon(self, filteredlist)
        
                
class GenCheck(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, highlightbackground="red", highlightcolor="red", highlightthickness=2)
        self.parent = parent
        self.Gen1 = tk.IntVar()
        self.Gen2 = tk.IntVar()
        self.Gen3 = tk.IntVar()
        self.Gen4 = tk.IntVar()
        self.Gen5 = tk.IntVar()
        self.Gen6 = tk.IntVar()
        self.Gen7 = tk.IntVar()
        self.Gen8 = tk.IntVar()
        self.Gen9 = tk.IntVar()
        tk.Checkbutton(self, text="Generation 1:    Kanto", variable=self.Gen1, font=("Bahnschrift SemiBold", 12)).grid(row=0, sticky="nsw", pady = 5, padx = 5)
        tk.Label(self, text = "Pokemon Red, Pokemon Blue, Pokemon Yellow", font=("Bahnschrift SemiBold", 8)).grid(row=1, sticky="nsw", pady = 5, padx = 5)

        tk.Checkbutton(self, text="Generation 2:    Johto", variable=self.Gen2, font=("Bahnschrift SemiBold", 12)).grid(row=2, sticky="nsw", pady = 5, padx = 5)
        tk.Label(self, text = "Pokemon Gold, Pokemon Silver, Pokemon Crystal", font=("Bahnschrift SemiBold", 8)).grid(row=3, sticky="nsw", pady = 5, padx = 5)

        tk.Checkbutton(self, text="Generation 3:    Hoenn", variable=self.Gen3, font=("Bahnschrift SemiBold", 12)).grid(row=4, sticky="nsw", pady = 5, padx = 5)
        tk.Label(self, text = "Pokemon Ruby, Pokemon Sapphire, Pokemon Emerald, Pokemon FireRed, Pokemon LeafGreen", font=("Bahnschrift SemiBold", 8)).grid(row=5, sticky="nsw", pady = 5, padx = 5)

        tk.Checkbutton(self, text="Generation 4:    Sinnoh", variable=self.Gen4, font=("Bahnschrift SemiBold", 12)).grid(row=6, sticky="nsw", pady = 5, padx = 5)
        tk.Label(self, text = "Pokemon Diamond, Pokemon Pearl, Pokemon Platinum, Pokemon HeartGold, Pokemon SoulSilver", font=("Bahnschrift SemiBold", 8)).grid(row=7, sticky="nsw", pady = 5, padx = 5)

        tk.Checkbutton(self, text="Generation 5:    Unova", variable=self.Gen5, font=("Bahnschrift SemiBold", 12)).grid(row=8, sticky="nsw", pady = 5, padx = 5)
        tk.Label(self, text = "Pokemon Black, Pokemon White, Pokemon Black 2, Pokemon White 2", font=("Bahnschrift SemiBold", 8)).grid(row=9, sticky="nsw", pady = 5, padx = 5)

        tk.Checkbutton(self, text="Generation 6:    Kalos", variable=self.Gen6, font=("Bahnschrift SemiBold", 12)).grid(row=10, sticky="nsw", pady = 5, padx = 5)
        tk.Label(self, text = "Pokemon X, Pokemon Y, Pokemon Omega Ruby, Pokemon Alpha Sapphire", font=("Bahnschrift SemiBold", 8)).grid(row=11, sticky="nsw", pady = 5, padx = 5)

        tk.Checkbutton(self, text="Generation 7:    Alola", variable=self.Gen7, font=("Bahnschrift SemiBold", 12)).grid(row=12, sticky="nsw", pady = 5, padx = 5)
        tk.Label(self, text = "Pokemon Sun, Pokemon Moon, Pokemon Ultra Sun, Pokemon Ultra Moon, Let's Go Pikachu, Let's Go Eevee", font=("Bahnschrift SemiBold", 8)).grid(row=13, sticky="nsw", pady = 5, padx = 5)

        tk.Checkbutton(self, text="Generation 8:    Galar, Hisui", variable=self.Gen8, font=("Bahnschrift SemiBold", 12)).grid(row=14, sticky="nsw", pady = 5, padx = 5)
        tk.Label(self, text = "Pokemon Sword, Pokemon Shield, Pokemon Legends Arceus, Pokemon Brilliant Diamond, Pokemon Shining Pearl", font=("Bahnschrift SemiBold", 8)).grid(row=15, sticky="nsw", pady = 5, padx = 5)

        tk.Checkbutton(self, text="Generation 9:    Paldea", variable=self.Gen9, font=("Bahnschrift SemiBold", 12)).grid(row=16, sticky="nsw", pady = 5, padx = 5)
        tk.Label(self, text = "Pokemon Scarlet, Pokemon Violet, Pokemon Legends Z-A", font=("Bahnschrift SemiBold", 8)).grid(row=17, sticky="nsw", pady = 5, padx = 5)
    
    def getGen(self):
        return [self.Gen1.get(), self.Gen2.get(), self.Gen3.get(), self.Gen4.get(), self.Gen5.get(), self.Gen6.get(), self.Gen7.get(), self.Gen8.get(), self.Gen9.get()]


class TypeCheck(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, highlightbackground="red", highlightcolor="red", highlightthickness=2)
        self.parent = parent

        self.Type = tk.IntVar()
        self.Type.set(1)

        self.grid_columnconfigure(0, weight=1, uniform="1")
        self.grid_columnconfigure(1, weight=1, uniform="1")

        self.grid_rowconfigure(0, weight=1, uniform="2")
        self.grid_rowconfigure(1, weight=1, uniform="2")
        self.grid_rowconfigure(2, weight=1, uniform="2")
        self.grid_rowconfigure(3, weight=1, uniform="2")
        self.grid_rowconfigure(4, weight=1, uniform="2")
        self.grid_rowconfigure(5, weight=1, uniform="2")
        self.grid_rowconfigure(6, weight=1, uniform="2")
        self.grid_rowconfigure(7, weight=1, uniform="2")
        self.grid_rowconfigure(8, weight=1, uniform="2")

        tk.Radiobutton(self, text = "Fire", variable=self.Type, value=1, font=("Bahnschrift SemiBold", 12)).grid(row = 0, column=0, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Water", variable=self.Type, value=2, font=("Bahnschrift SemiBold", 12)).grid(row = 0, column=1, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Grass", variable=self.Type, value=3, font=("Bahnschrift SemiBold", 12)).grid(row = 1, column=0, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Electric", variable=self.Type, value=4, font=("Bahnschrift SemiBold", 12)).grid(row = 1, column=1, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Psychic", variable=self.Type, value=5, font=("Bahnschrift SemiBold", 12)).grid(row = 2, column=0, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Ice", variable=self.Type, value=6, font=("Bahnschrift SemiBold", 12)).grid(row = 2, column=1, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Dragon", variable=self.Type, value=7, font=("Bahnschrift SemiBold", 12)).grid(row = 3, column=0, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Dark", variable=self.Type, value=8, font=("Bahnschrift SemiBold", 12)).grid(row = 3, column=1, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Fairy", variable=self.Type, value=9, font=("Bahnschrift SemiBold", 12)).grid(row = 4, column=0, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Normal", variable=self.Type, value=10, font=("Bahnschrift SemiBold", 12)).grid(row = 4, column=1, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Fighting", variable=self.Type, value=11, font=("Bahnschrift SemiBold", 12)).grid(row = 5, column=0, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Flying", variable=self.Type, value=12, font=("Bahnschrift SemiBold", 12)).grid(row = 5, column=1, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Poison", variable=self.Type, value=13, font=("Bahnschrift SemiBold", 12)).grid(row = 6, column=0, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Ground", variable=self.Type, value=14, font=("Bahnschrift SemiBold", 12)).grid(row = 6, column=1, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Rock", variable=self.Type, value=15, font=("Bahnschrift SemiBold", 12)).grid(row = 7, column=0, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Bug", variable=self.Type, value=16, font=("Bahnschrift SemiBold", 12)).grid(row = 7, column=1, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Ghost", variable=self.Type, value=17, font=("Bahnschrift SemiBold", 12)).grid(row = 8, column=0, padx = 5, pady = 5, sticky="nsw")
        tk.Radiobutton(self, text = "Steel", variable=self.Type, value=18, font=("Bahnschrift SemiBold", 12)).grid(row = 8, column=1, padx = 5, pady = 5, sticky="nsw")
    
    def getType(self):
        match self.Type.get():
            case 0:
                return ""
            case 1:
                return "fire"
            case 2:
                return "fater"
            case 3:
                return "grass"
            case 4:
                return "electric"
            case 5:
                return "psychic"
            case 6:
                return "ice"
            case 7:
                return "dragon"
            case 8:
                return "dark"
            case 9:
                return "fairy"
            case 10:
                return "normal"
            case 11:
                return "fighting"
            case 12:
                return "flying"
            case 13:
                return "poison"
            case 14:
                return "ground"
            case 15:
                return "rock"
            case 16:
                return "rug"
            case 17:
                return "ghost"
            case 18:
                return "steel"

#Main, initialize Tk objects and loop
if __name__ == "__main__":
    pokedex = Pokedex()
    pokedex.mainloop()