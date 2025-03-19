import tkinter as tk

class Pokedex(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Pokedex")
        self.geometry("1280x720")
        self.minsize(1280,720)
        self.maxsize(1280,720)

        rootwindow = tk.Frame(self)
        rootwindow.grid(row=0, column=0, sticky="nsew")

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
        label = tk.Label(self, text="Start page")
        label.grid(row=0, column=0)

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