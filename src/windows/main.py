import tkinter as tk
from tkinter import ttk
from src.controllers import main_controller

frame_color = '#575555'
background_color = '#2a2a2a'

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('SISTEMA DE RECIBOS')
        self.resizable(True, True)
        self.minsize(800, 600)
        self.config(
            background= background_color,
            padx=20,
            pady=20
        )
        self.grid()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=10)

        self.enterprise_frame = EnterpriseFrame(self)
        self.enterprise_frame.grid(
            row=0, column=0, sticky="nsew", pady=20,
        )
        self.actions_frame = ActionsFrame(self)
        self.actions_frame.grid(
            row=1, column=0, sticky="nsew",
        )
        self.registers_frame = ReceiptsFrame(self)
        self.registers_frame.grid(
            row=2, column=0, sticky="nsew", pady=20,
        )

class EnterpriseFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.config(
            background=frame_color,
            padx=20,
            pady=20,
        )        
        tk.Label(self, text='Enterprise LOGO').grid(row=0, column=0)
        tk.Label(self, text='Enterprise INFO').grid(row=0, column=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4) 

class ActionsFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.config(
            background=frame_color,
            padx=20,
            pady=20
        )        
        
        self.new_receipt_button = tk.Button(
            self,
            text='Adicionar',
            command=main_controller.show_new_receipt_window
        )
        tk.Label(self, text='Imagem').grid(row=0, column=0)
        tk.Label(self, text='Imagem').grid(row=0, column=1)
        tk.Label(self, text='Imagem').grid(row=0, column=2)
        tk.Label(self, text='Imagem').grid(row=0, column=3)
        self.new_receipt_button.grid(row=1, column=0)
        self.edit_receipt = tk.Button(
            self,
            text='Editar',
            command=main_controller.show_edit_receipt_window
        )
        self.edit_receipt.grid(row=1, column=1)
        self.search_receipt = tk.Button(
            self,
            text='Buscar',
            command=main_controller.show_search_receipt_window
        )
        self.search_receipt.grid(row=1, column=2)
        self.print_receipt = tk.Button(
            self,
            text='Imprimir'
        )
        self.print_receipt.grid(row=1, column=3)

class ReceiptsFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)               
        
        self.config(background=frame_color)

        self.create_table()

    def create_table(self):

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(self, orient="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree = ttk.Treeview(
            self,
            columns=("Número", "Data", "Valor", "Cliente", "Devedor"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("Número", text="Número")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Devedor", text="Devedor")

        self.tree.column("Número", width=30)
        self.tree.column("Data", width=80)
        self.tree.column("Valor", width=80)
        self.tree.column("Cliente", width=200)
        self.tree.column("Devedor", width=200)

        dados = [
            (1, "2025-05-27", "R$ 100,00", "L.J Guerra", "Maycon Santos LTDA"),
            
        ]

        for item in dados:
            self.tree.insert("", tk.END, values=item)
        

if __name__ == '__main__':
    main_window  = MainWindow() 
    main_window.mainloop()

