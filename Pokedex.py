import tkinter as tk
import json
from PIL import ImageTk, Image
from PokemonPage import PokemonPage
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
        AdvancedSearchButton = tk.Button(Searchbar, text = "Advanced Search[TEST RN]", font=("Bahnschrift SemiBold", 10), width=20, command=self.PokemonEntry)
        AdvancedSearchButton.grid(row = 1, column=1, sticky="nw", padx = 10)
        
        #Red Footer
        Footer = tk.Frame(self, bg = "red", height=5)
        Footer.grid(row=3, column=0, sticky="nsew")
        Footer.grid_rowconfigure(0, weight=1)
    
    def searchbutton(self):
        self.controller.topPage("Search")
        self.controller.passSearch(self.usersearch.get())


    #Test function currently in so I have easy access to the Pokemon page, bypassing the search function right now
    def PokemonEntry(self, str = "goodra"):
        PokePage = PokemonPage(self, str)
        

#Frame that shows the results of the search algorithm
class Search(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.searchentry = tk.StringVar()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        Header = tk.Frame(self, bg = "red", height = 10 )
        Header.grid(row = 0, column=0,sticky="nsew", columnspan=3)

        Button = tk.Button(self, text = "<-- Start", font=("Bahnschrift SemiBold", 10), width = 20, command = lambda:self.controller.topPage("Start"))
        Button.grid(row = 1, column = 0, sticky="nw", padx=10, pady=10)

        PageName = tk.Label(self, text = "Search", font=("Bahnschrift SemiBold", 15))
        PageName.grid(row = 1, column = 1, sticky="we", padx=10, pady=10)

        Button = tk.Button(self, text = "Advanced Search -->", font=("Bahnschrift SemiBold", 10), width = 20, command = lambda:self.controller.topPage("AdvancedSearch"))
        Button.grid(row = 1, column = 2, sticky="ne", padx=10, pady=10)

        borderframe = tk.Frame(self, highlightbackground="red", highlightcolor="red", highlightthickness=2)
        borderframe.grid(row = 2, column=0, columnspan=3, sticky="nsew", padx = 5, pady = 5)
        borderframe.grid_columnconfigure(0, weight = 1)
        borderframe.grid_rowconfigure(0, weight = 1)

        self.searchframe = SearchFrame(borderframe, self.searchentry.get())
        self.searchframe.grid(row = 0, column = 0, sticky="nsew")

        Footer = tk.Frame(self, bg = "red", height = 10 )
        Footer.grid(row = 3, column=0,sticky="nsew", columnspan=3)

    def update_search_entry(self, entry):
        self.searchentry.set(entry)
        self.searchframe.destroy()
        self.searchframe = SearchFrame(self.searchframe.master, self.searchentry.get())
        self.searchframe.grid(row = 0, column = 0, sticky="nsew")
        #self.controller.update()
        
class SearchFrame(tk.Frame):
    def __init__(self, parent, searchentry):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.searchentry = tk.StringVar()
        self.searchentry.set(searchentry)
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        #Searchbar
        Bar = tk.Entry(self, width=85, font=("Bahnschrift SemiBold", 15), textvariable=self.searchentry)
        Bar.grid(row=0,column=0, padx = 10, pady = 10)

        Button = tk.Button(self, text = "Search", font=("Bahnschrift SemiBold", 10), width = 10, command=self.updatesearch)
        Button.grid(row = 0, column = 1, sticky="we", padx=10, pady=10)

        Seperator = tk.Frame(self, bg = "red", height = 2 )
        Seperator.grid(row = 1, column=0, sticky="nsew", columnspan=2, padx = 5, pady = 5)

        self.borderframe = tk.Frame(self)
        self.borderframe.grid(row = 2, column=0, columnspan=2, sticky="nsew", padx = 5, pady = 5)
        self.borderframe.grid_columnconfigure(0, weight = 1)
        self.borderframe.grid_columnconfigure(1, weight = 1)
        self.borderframe.grid_rowconfigure(0, weight = 1)
        self.borderframe.grid_rowconfigure(1, weight = 1)
        self.borderframe.grid_rowconfigure(2, weight = 1)
        
        self.searchresults = self.get6results(self.searchentry.get())
        count = 0
        self.results = []
        for i in self.searchresults:
            box = SearchResult(self.borderframe, i)
            box.grid(row=count//2,column=count%2,padx=20,pady=10, sticky = "nsew")
            box.grid_propagate(False)
            self.results.append(box)
            count+=1
    
    def updatesearch(self):
        self.searchresults = self.get6results(self.searchentry.get())
        counter = 0
        print(len(self.results))
        print(len(self.searchresults))
        if len(self.results) > 0 :
            print("made it")
            if len(self.searchresults) == 0:
                print("made it 2")
                for i in self.results:
                    print("made it 3")
                    i.destroy()
                    print(len(self.results))
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
        else:
            count = 0
            print("empty")
            for i in self.searchresults:
                box = SearchResult(self.borderframe, i)
                box.grid(row=count//2,column=count%2,padx=20,pady=10, sticky = "nsew")
                box.grid_propagate(False)
                self.results.append(box)
                count+=1

    def get6results(self, searched):
        justNames = []
        pokemonNames = {}
        if searched != "":
            with open('AllPokemon.json', 'r') as file:
                AllPokemon = file.read()
                AllPokemondict = json.loads(AllPokemon)
            counter = 0
            for pokemon in AllPokemondict['results']:
                similarity = SequenceMatcher(None, searched.casefold(), pokemon['name'].casefold()).ratio()
                if counter < 6:
                    pokemonNames[pokemon['name']] = similarity
                    sorted_dict = sorted(pokemonNames.items(), key=lambda item: item[1])
                    pokemonNames = dict(sorted_dict)
                    counter+=1
                elif counter == 6:
                    first = next(iter(pokemonNames))
                    if pokemonNames[first] < similarity:
                        pokemonNames[pokemon['name']] = similarity
                        pokemonNames.pop(first)
                        sorted_dict = sorted(pokemonNames.items(), key=lambda item: item[1])
                        pokemonNames = dict(sorted_dict)
            justNames = list(pokemonNames.keys())
            justNames.reverse()
        print(justNames)
        return justNames



                
    
    
class SearchResult(tk.Frame):

    def __init__(self, parent, pokemonname):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.pokemoname = pokemonname


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        Name = tk.Label(self, text = self.pokemoname.capitalize(), font=("Bahnschrift SemiBold", 15), width= 40, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        Name.grid(row = 0, column = 0, sticky="nsew", padx=5, pady=5)

        Open = tk.Button(self, text = "Go", font=("Bahnschrift SemiBold", 10), width = 5, command = self.PokemonEntry)
        Open.grid(row = 0, column = 1, sticky="we", padx=5, pady=5)

    
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
        borderframe.grid_columnconfigure(0, weight = 1)
        borderframe.grid_rowconfigure(0, weight = 1)

        Footer = tk.Frame(self, bg = "red", height = 10 )
        Footer.grid(row = 3, column=0,sticky="nsew", columnspan=3)



#Main, initialize Tk objects and loop
if __name__ == "__main__":
    pokedex = Pokedex()
    pokedex.mainloop()