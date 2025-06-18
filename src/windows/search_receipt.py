from .main import tk, ttk
from tkinter import messagebox
from src.windows.theme.custom import ArcEntry

class SearchReceiptWindow(tk.Toplevel):
    def __init__(self, wm,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm = wm
        self.title('Buscar Recibo')
        self.configure(
            background='#F5F6F7',
            padx=20,
            pady=20,
        )

        self.search_receipt_form = SearchReceiptForm(master=self, wm=self.wm)
        self.search_receipt_form.grid(row=0, column=0, sticky='w',)

        self.actions_search_receipt = ActionsSearchReceipt(master=self, wm=self.wm)
        self.actions_search_receipt.grid(row=0, column=0, sticky='e')

        self.result_tree = self.create_table()
        self.result_tree.grid(row=1, column=0, sticky='wnes')

        self.grid_columnconfigure(0, weight=1)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        

    def create_table(self):

        scrollbar = ttk.Scrollbar(self, orient="vertical")
        scrollbar.grid(row=1, column=1, sticky="ns")

        self.tree = ttk.Treeview(
            self,
            columns=("Número", "Data", "Valor", "Cliente", "Devedor"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Return>", self.on_double_click)
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("Número", text="Número", anchor="w")
        self.tree.heading("Data", text="Emissão", anchor="w")
        self.tree.heading("Valor", text="Valor", anchor="w")
        self.tree.heading("Cliente", text="Cliente", anchor="w")
        self.tree.heading("Devedor", text="Devedor", anchor="w")

        self.tree.column("Número", width=100)
        self.tree.column("Data", width=120)
        self.tree.column("Valor", width=150)
        self.tree.column("Cliente", width=250)
        self.tree.column("Devedor", width=250)

        return self.tree
    
    def clear_treeview(self):
        for item in self.result_tree.get_children():
            print('deleting')
            self.result_tree.delete(item)

    def on_double_click(self,event):
        item = self.result_tree.focus()
        if item:            
            receipt = self.wm.controller.get_receipt(item)
            print(receipt)
            self.wm.show_edit_receipt_window(receipt.__data__, master=self)
            
            self.wm.root.receipts_frame.tree.selection_set(item)
            self.wm.root.receipts_frame.tree.focus(item)
            self.wm.root.receipts_frame.tree.see(item)
    
    def search(self, event=None):
        if self.tree.get_children():
            self.clear_treeview()

        data = {
            field_name:entry.get()
            for field_name, entry 
            in self.search_receipt_form.inputs.items()
        }
        
        if (
            not data['Cliente'] and
            not data['Devedor'] and
            not data['Data de Criação']
        ):
            messagebox.showinfo(
                message='Preencha pelomenos um campo de pesquisa'
            )
            return

        try:
            receipts = self.wm.controller.search_receipts(
                client=data.get('Cliente'),
                debtor=data.get('Devedor'),
                date=data.get('Data de Criação')
            )
        except ValueError as err:
            if 'time data' in str(err):
                messagebox.showerror(title='Erro',message=f'Data inválida')
                self.search_receipt_form.inputs['Data de Criação'].delete(0,tk.END)
            return
        except Exception as err:
            messagebox.showerror(title='Erro',message=str(err))
            return
        
        if not receipts:
            messagebox.showinfo(
                message='Nenhuma correspondência encontrada'
            )
            return

        for item in receipts:
            print(item)
            self.result_tree.insert("", tk.END, values=item, iid=item[0])    

    def refresh_tree(self):
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        print('search')
    
        data = self.wm.controller.get_all_receipts()

        for item in data:
            self.result_tree.insert("", tk.END, values=item, iid=item[0])

class SearchReceiptForm(ttk.Frame):
    def __init__(self, wm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm = wm
        self.inputs = {}

        fields = [
            "Cliente",
            "Devedor",
            "Data de Criação"
        ]

        for i, field_name in enumerate(fields):
            label = ttk.Label(self, text=field_name)
            label.grid(row=i, column=0, sticky='nsew', padx=10)

            field = ArcEntry(self, text=field_name)
            field.grid(row=i, column=1, sticky='nsew', pady=5)
            field.bind("<Return>", self.master.search)
            self.inputs[field_name] = field

class ActionsSearchReceipt(ttk.Frame):
    def __init__(self, wm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm = wm
        self.buttons = {}

        buttons = [
            'Buscar'
        ]

        for i, button_name in enumerate(buttons):
            button = ttk.Button(self, text=button_name)
            button.grid(row=0, column=i, sticky='nsew')
            self.buttons[button_name] = button

        self.search_button: ttk.Button = self.buttons['Buscar']
        self.search_button.configure(command=self.master.search)