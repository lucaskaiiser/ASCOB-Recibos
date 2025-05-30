from .main import tk, ttk

class SearchReceiptWindow(tk.Toplevel):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Buscar Recibo')
        self.geometry('800x600')

        self.search_receipt_form = SearchReceiptForm(self)
        self.search_receipt_form.grid(row=0, column=0, sticky='nsew')

        self.actions_search_receipt = ActionsSearchReceipt(self)
        self.actions_search_receipt.grid(row=1, column=0, sticky='nsew')

        self.result_text = tk.Text(self, height=10, width=50, state='disabled')
        self.result_text.grid(row=2, column=0)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

class SearchReceiptForm(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.inputs = {}

        fields = [
            "Cliente",
            "Número do Boleto",
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

