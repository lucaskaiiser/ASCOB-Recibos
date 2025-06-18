import tkinter as tk
from tkinter import ttk

class ArcEntry(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(
            master, 
            background="#CCCCCC", 
            bd=0, 
            padx=5, 
            pady=5, 
            bg="white",
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor="#cccccc",
        )

        self.entry = tk.Entry(
            self,
            font=("Arial", 10),
            bg="white",
            fg="black",
            relief="flat",
            insertbackground="black",
            **kwargs
        )
        self.entry.pack(fill="both", expand=True)

        self.entry.bind("<FocusIn>", self.on_focus)
        self.entry.bind("<FocusOut>", self.on_blur)
        

    def on_focus(self, event):
        self.entry.config(bg="gold")
        self.config(bg="gold")  

    def on_blur(self, event):
        self.entry.config(bg="white")  
        self.config(bg="white")

    
    def get(self): return self.entry.get()
    def insert(self, index, value): self.entry.insert(index, value)
    def delete(self, start, end=None): self.entry.delete(start, end)
    def focus(self): self.entry.focus()
    def bind(self, *args, **kwargs): self.entry.bind(*args, **kwargs)  


class ArcText(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(
            master, 
            background="#CCCCCC", 
            bd=0, 
            padx=5, 
            pady=5, 
            bg="white",
            highlightthickness=1,
            highlightbackground="#cccccc",
            highlightcolor="#cccccc",
        )

        self.text = tk.Text(
            self,
            bg="white",
            fg="black",
            font=("Arial", 10),
            relief="flat",
            insertbackground="black",
            borderwidth=0,
            highlightthickness=0,
            **kwargs
        )
        self.text.pack(fill="both", expand=True)

        self.text.bind("<FocusIn>", self.on_focus)
        self.text.bind("<FocusOut>", self.on_blur)

    def on_focus(self, event):
        self.text.config(bg="gold")
        self.config(bg="gold")

    def on_blur(self, event):
        self.text.config(bg="white")
        self.config(bg="white")

    def get(self, index1="1.0", index2="end-1c"):
        return self.text.get(index1, index2)

    def insert(self, index, value):
        self.text.insert(index, value)

    def delete(self, index1, index2=None):
        self.text.delete(index1, index2)

    def focus(self):
        self.text.focus()

    def bind(self, *args, **kwargs):
        self.text.bind(*args, **kwargs)