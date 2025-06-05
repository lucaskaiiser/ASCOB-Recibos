from .main import tk, ttk
from src.controllers import main_controller

class SearchReceiptWindow(tk.Toplevel):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Buscar Recibo')

        self.search_receipt_form = SearchReceiptForm(self)
        self.search_receipt_form.grid(row=0, column=0)

        self.actions_search_receipt = ActionsSearchReceipt(self)
        self.actions_search_receipt.grid(row=1, column=0)

        self.result_tree = self.create_table()
        self.result_tree.grid(row=2, column=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def create_table(self):

        scrollbar = ttk.Scrollbar(self, orient="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree = ttk.Treeview(
            self,
            columns=("Número", "Data", "Valor", "Cliente", "Devedor"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<Double-1>", self.on_double_click)
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
            self.tree.insert("", tk.END, values=item, iid=item[0])

        return self.tree
    
    def on_double_click(self,event):
        item = self.tree.focus()
        print(item)
        if item:
            from src.controllers.main_controller import show_edit_receipt_window
            self.destroy()
            receipt = main_controller.get_receipt(item[0])
            print(receipt.__data__)
            show_edit_receipt_window()
        

class SearchReceiptForm(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.inputs = {}

        fields = [
            "Cliente",
            "Devedor",
            "Data do Pagamento"
        ]

        for i, field_name in enumerate(fields):
            label = tk.Label(self, text=field_name)
            label.grid(row=i, column=0, sticky='nsew')

            field = tk.Entry(self, text=field_name)
            field.grid(row=i, column=1, sticky='nsew')
            self.inputs[field_name] = field


class ActionsSearchReceipt(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buttons = {}

        buttons = [
            'Buscar'
        ]

        for i, button_name in enumerate(buttons):
            button = tk.Button(self, text=button_name)
            button.grid(row=0, column=i, sticky='nsew')
            self.buttons[button_name] = button

