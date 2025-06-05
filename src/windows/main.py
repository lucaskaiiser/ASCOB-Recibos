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
        self.receipts_frame = ReceiptsFrame(self)
        self.receipts_frame.grid(
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
        tk.Label(self, text='Imagem').grid(row=0, column=2)
        tk.Label(self, text='Imagem').grid(row=0, column=3)
        self.new_receipt_button.grid(row=1, column=0)
        
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

        self.tree = self.create_table()

    def create_table(self):

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(self, orient="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns")

        tree = ttk.Treeview(
            self,
            columns=("Número", "Data", "Valor", "Cliente", "Devedor"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=tree.yview)

        tree.heading("Número", text="Número")
        tree.heading("Data", text="Data")
        tree.heading("Valor", text="Valor")
        tree.heading("Cliente", text="Cliente")
        tree.heading("Devedor", text="Devedor")

        tree.column("Número", width=30)
        tree.column("Data", width=80)
        tree.column("Valor", width=80)
        tree.column("Cliente", width=200)
        tree.column("Devedor", width=200)
        tree.bind("<Double-1>", self.on_double_click)

        data = main_controller.get_all_receipts().tuples()

        for item in data:
            tree.insert("", tk.END, values=item, iid=item[0])
        return tree
    
    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
        data = main_controller.get_all_receipts().tuples()

        for item in data:
            self.tree.insert("", tk.END, values=item, iid=item[0])

    def on_double_click(self,event):
        item = self.tree.focus()
        if item:
            print(item)
            from src.controllers.main_controller import show_edit_receipt_window
            receipt = main_controller.get_receipt(item)
            show_edit_receipt_window(receipt.__data__)
    
class ReceiptTreeView(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.heading("Número", text="Número")
        self.heading("Data", text="Data")
        self.heading("Valor", text="Valor")
        self.heading("Cliente", text="Cliente")
        self.heading("Devedor", text="Devedor")

        self.column("Número", width=30)
        self.column("Data", width=80)
        self.column("Valor", width=80)
        self.column("Cliente", width=200)
        self.column("Devedor", width=200)

        data = main_controller.get_all_receipts().tuples()

        for item in data:
            self.insert("", tk.END, values=item)


if __name__ == '__main__':
    main_window  = MainWindow()
    main_window.mainloop()

