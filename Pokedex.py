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
            print(pagename)
            frame = page(parent=rootwindow, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[pagename] = frame
        print(len(self.pages))
        
        #Set the starting frame to Start
        self.topPage("Start")
    
    #raise the selected frame
    def topPage(self, pagename):
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
        Bar = tk.Entry(Searchbar, width=75)
        Bar.grid(row=0,column=0, columnspan=2)

        #Search Button
        SearchButton = tk.Button(Searchbar, text = "Search", width=20, command = lambda:self.controller.topPage("Search"))
        SearchButton.grid(row=1, column=0, sticky="ne", padx = 10)

        #Advanced Search button
        AdvancedSearchButton = tk.Button(Searchbar, text = "Advanced Search[TEST RN]", width=20, command=self.PokemonEntry)
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

        
        self.grid_rowconfigure(4, weight=1)

        Header = tk.Frame(self, bg = "red", height = 5)
        Header.grid(row = 0, column=0)

        Button = tk.Button(self, text = "<-- Start", width = 20, command = lambda:self.controller.topPage("Start"))
        Button.grid(row = 1, column = 0)

        label = tk.Label(self, text = "Search Page")
        label.grid(row=2, column=0)

#Filter search Frame for getting a list of  results aligning with selected filters
class AdvancedSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Advanced Search Page")
        label.grid(row=0, column=0)


#Main, initialize Tk objects and loop
if __name__ == "__main__":
    pokedex = Pokedex()
    pokedex.mainloop()