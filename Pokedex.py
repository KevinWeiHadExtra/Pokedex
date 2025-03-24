import tkinter as tk
from PIL import ImageTk, Image
from PokemonPage import PokemonPage

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
        if pagename == "Search":
            self.pages[pagename].update_search_entry("bulbasaur")
        frame = self.pages[pagename]
        frame.tkraise()

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

        #Searchbar
        Bar = tk.Entry(Searchbar, width=75, font=("Bahnschrift SemiBold", 10))
        Bar.grid(row=0,column=0, columnspan=2)

        #Search Button
        SearchButton = tk.Button(Searchbar, text = "Search", font=("Bahnschrift SemiBold", 10), width=20, command = lambda:self.controller.topPage("Search"))
        SearchButton.grid(row=1, column=0, sticky="ne", padx = 10)

        #Advanced Search button
        AdvancedSearchButton = tk.Button(Searchbar, text = "Advanced Search[TEST RN]", font=("Bahnschrift SemiBold", 10), width=20, command=self.PokemonEntry)
        AdvancedSearchButton.grid(row = 1, column=1, sticky="nw", padx = 10)
        
        #Red Footer
        Footer = tk.Frame(self, bg = "red", height=5)
        Footer.grid(row=3, column=0, sticky="nsew")
        Footer.grid_rowconfigure(0, weight=1)
    
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

        searchframe = SearchFrame(borderframe, self.searchentry)
        searchframe.grid(row = 0, column = 0, sticky="nsew")

        Footer = tk.Frame(self, bg = "red", height = 10 )
        Footer.grid(row = 3, column=0,sticky="nsew", columnspan=3)

    def update_search_entry(self, entry):
        self.searchentry = entry
        
class SearchFrame(tk.Frame):
    def __init__(self, parent, searchentry):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.searchentry = searchentry
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        #Searchbar
        Bar = tk.Entry(self, width=85, font=("Bahnschrift SemiBold", 15))
        Bar.grid(row=0,column=0, padx = 10, pady = 10)

        Button = tk.Button(self, text = "Search", font=("Bahnschrift SemiBold", 10), width = 10)
        Button.grid(row = 0, column = 1, sticky="we", padx=10, pady=10)

        Seperator = tk.Frame(self, bg = "red", height = 2 )
        Seperator.grid(row = 1, column=0, sticky="nsew", columnspan=2, padx = 5, pady = 5)

        borderframe = tk.Frame(self)
        borderframe.grid(row = 2, column=0, columnspan=2, sticky="nsew", padx = 5, pady = 5)
        borderframe.grid_columnconfigure(0, weight = 1)
        borderframe.grid_columnconfigure(1, weight = 1)
        borderframe.grid_rowconfigure(0, weight = 1)
        borderframe.grid_rowconfigure(1, weight = 1)
        borderframe.grid_rowconfigure(2, weight = 1)

        result1 = SearchResult(borderframe, "bulbasaur")
        result1.grid(row=0,column=0,padx=20,pady=10, sticky = "nsew")
        result1.grid_propagate(False)

        result2 = SearchResult(borderframe, "bulbasaur")
        result2.grid(row=0,column=1,padx=20,pady=10, sticky = "nsew")
        result2.grid_propagate(False)

        result3 = SearchResult(borderframe, "bulbasaur")
        result3.grid(row=1,column=0,padx=20,pady=10, sticky = "nsew")
        result3.grid_propagate(False)
    
    def test(self):
        self.update()
        print(self.result1.winfo_height())
        print(self.result1.winfo_width())
        
    
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