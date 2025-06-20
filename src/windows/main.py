import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from pathlib import Path

base_dir = Path(__file__).parent.parent.parent

frame_color = '#575555'
background_color = '#F5F6F7'

class MainWindow(ThemedTk):
    
    def __init__(self, wm, *args, **kwargs):
        super().__init__(theme='arc', *args, **kwargs)

        self.withdraw()

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=40)  
        style.configure("Treeview.Heading", font=("Arial", 10))
        style.configure("TButton", focuscolor="ffffff")
        style.configure("TLabel", font=("Arial", 10))
        

        style.map("Treeview",
            foreground=[("selected", "black")],
            background=[("selected", "#CBDFEE")]
        )
    
        icon = ImageTk.PhotoImage(file=str(base_dir / 'static' / 'pngegg.ico'))
        self.iconphoto(True, icon)

        self.wm = wm
        self.title('ASCOB Recibos')
        self.resizable(True, True)
        self.minsize(1200, 600)

        self.config(
            background=background_color,
            padx=20,
            pady=20
        )
        self.grid()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=10)

        self.enterprise_frame = EnterpriseFrame(master=self, wm=self.wm)
        self.enterprise_frame.grid(row=0, column=0, sticky="nsew", pady=10)

        self.receipts_frame = ReceiptsFrame(master=self, wm=self.wm)
        self.receipts_frame.grid(row=2, column=0, sticky="nsew", pady=10)

        self.actions_frame = ActionsFrame(master=self, wm=self.wm)
        self.actions_frame.grid(row=1, column=0, sticky="nsew")

        self.after(100, self._center_and_show)
    
    def _center_and_show(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.deiconify()  # Exibe a janela centralizada
        self.focus_force()

class EnterpriseFrame(ttk.Frame):
    def __init__(self, wm, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.wm = wm
        
        self.logo = Image.open(str(base_dir / 'static' / 'pngegg.png'))
        self.logo = self.logo.resize((80, 60))
        self.logo = ImageTk.PhotoImage(self.logo)

        self.image = tk.Label(self, image=self.logo)
        self.image.configure(
            background=background_color
        )
        self.image.grid(row=0, column=0, sticky='wns')
        ttk.Label(
            self,
            text='ASCOB - Sistema de Armazenamento e Emissão de Recibos',
            font=('Arial', 14) 
            
        ).grid(row=0, column=1, sticky='sn')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4) 

class ActionsFrame(ttk.Frame):
    def __init__(self, wm, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.wm = wm          
        
        self.new_receipt_button = ttk.Button(
            self,
            text='Novo Recibo',
            command=lambda: self.wm.show_new_receipt_window(master = self.master)
        )
        self.new_image = Image.open(str(base_dir / 'static' /'new.png'))
        self.new_image = ImageTk.PhotoImage(self.new_image)
            
        ttk.Label(self, image=self.new_image).grid(row=0, column=0)

        self.search_image = Image.open(str(base_dir / 'static' / 'search.png'))
        self.search_image = ImageTk.PhotoImage(self.search_image)
            
        ttk.Label(self, image=self.search_image).grid(row=0, column=2)

        self.print_image = Image.open(str(base_dir / 'static' / 'print.png'))
        self.print_image = ImageTk.PhotoImage(self.print_image)
            
        ttk.Label(self, image=self.print_image).grid(row=0, column=3)
        
        self.new_receipt_button.grid(row=1, column=0,padx=10)
        
        self.search_receipt = ttk.Button(
            self,
            text='Buscar',
            command=lambda: self.wm.show_search_receipt_window(master = self.master),
            style='custom.TButton',
        )
        self.search_receipt.grid(row=1, column=2, padx=10)
        self.print_receipt = ttk.Button(
            self,
            text='Imprimir',
            command=self.master.receipts_frame.print_receipt
        )
        self.print_receipt.grid(row=1, column=3, padx=10)

        self.configure(
            padding=20
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

class ReceiptsFrame(ttk.Frame):
    def __init__(self, wm,*args, **kwargs):
        super().__init__(*args, **kwargs)               
        self.wm = wm
        

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

        tree.heading("Número", text="Número", anchor="w")
        tree.heading("Data", text="Criação", anchor="w")
        tree.heading("Valor", text="Valor", anchor="w")
        tree.heading("Cliente", text="Cliente", anchor="w")
        tree.heading("Devedor", text="Devedor", anchor="w")

        tree.column("Número", width=30)
        tree.column("Data", width=80)
        tree.column("Valor", width=80)
        tree.column("Cliente", width=200)
        tree.column("Devedor", width=200)
        tree.bind("<Double-1>", self.on_double_click)
        tree.bind("<Return>", self.on_double_click)

        data = self.wm.controller.get_all_receipts()

        for item in data:
            tree.insert("", tk.END, values=item, iid=item[0])
        return tree
    
    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
        data = self.wm.controller.get_all_receipts()

        for item in data:
            self.tree.insert("", tk.END, values=item, iid=item[0])

    def on_double_click(self,event):
        item = self.tree.focus()
        if item:
            print(item)
            receipt = self.wm.controller.get_receipt(item)
            self.wm.show_edit_receipt_window(receipt.__data__,master = self.master)
    
    def print_receipt(self):
        item = self.tree.focus()
        if item:
            receipt = self.wm.controller.get_receipt(item)
            confirmation = messagebox.askyesno(
                message=f'Confirmar impressão do recibo {receipt.id}?'
            )
            if confirmation:
                self.wm.controller.print_pdf(receipt.__data__)
        else:
            messagebox.showinfo(message='Nenhum recibo selecionado')
            
    
class ReceiptTreeView(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.heading("Número", text="Número")
        self.heading("Data", text="Emissão")
        self.heading("Valor", text="Valor")
        self.heading("Cliente", text="Cliente")
        self.heading("Devedor", text="Devedor")

        self.column("Número", width=40)
        self.column("Data", width=80)
        self.column("Valor", width=80)
        self.column("Cliente", width=200)
        self.column("Devedor", width=200)

        data = self.wm.controller.get_all_receipts().tuples()

        for item in data:
            self.insert("", ttk.END, values=item)

