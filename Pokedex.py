import tkinter as tk
from PIL import ImageTk, Image

class Pokedex(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title("Pokedex")
        self.geometry("1280x720")
        self.minsize(1280,720)
        self.maxsize(1280,720)

        rootwindow = tk.Frame(self)
        rootwindow.grid(row=0, column=0, sticky="nsew")
        rootwindow.grid_rowconfigure(0, weight=1)
        rootwindow.grid_columnconfigure(0, weight=1)
        rootwindow.configure(bg = "purple")

        self.configure(bg="red")
        self.pages = {}
        for page in (Start, Search, AdvancedSearch):
            pagename = page.__name__
            frame = page(parent=rootwindow, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[pagename] = frame
        
        self.topPage("Start")
    
    def topPage(self, pagename):
        frame = self.pages[pagename]
        frame.tkraise()


class Start(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="blue")

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1, uniform="topdown")
        self.rowconfigure(1, weight = 1, uniform="center")
        self.rowconfigure(2, weight = 1, uniform="center")
        self.rowconfigure(3, weight = 1, uniform="topdown")

        Header = tk.Frame(self, bg = "red", height=5)
        Header.grid(row=0, column=0, sticky="nsew")
        Header.grid_rowconfigure(0, weight=1)
        
        self.PokedexPic = ImageTk.PhotoImage(Image.open("PokedexLogo.png"))
        Logo = tk.Label(self, image=self.PokedexPic)
        Logo.grid(row = 1, column=0, sticky="nsew")

        Searchbar = tk.Frame(self)
        Searchbar.grid(row= 2, column=0, sticky="nsew")
        Searchbar.grid_rowconfigure(0, weight=1)
        Searchbar.grid_rowconfigure(1, weight=1)
        Searchbar.grid_columnconfigure(0, weight=1)
        Searchbar.grid_columnconfigure(1, weight=1)

        Bar = tk.Entry(Searchbar, width=75)
        Bar.grid(row=0,column=0, columnspan=2)
        
        SearchButton = tk.Button(Searchbar, text = "Search", width=20)
        SearchButton.grid(row=1, column=0, sticky="ne", padx = 10)
        AdvancedSearchButton = tk.Button(Searchbar, text = "Advanced Search", width=20)
        AdvancedSearchButton.grid(row = 1, column=1, sticky="nw", padx = 10)
        
        Footer = tk.Frame(self, bg = "red", height=5)
        Footer.grid(row=3, column=0, sticky="nsew")
        Footer.grid_rowconfigure(0, weight=1)

        


class Search(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        label = tk.Label(self, text = "Search Page")
        label.grid(row=0, column=0)

class AdvancedSearch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Advanced Search Page")
        label.grid(row=0, column=0)



if __name__ == "__main__":
    pokedex = Pokedex()
    pokedex.mainloop()