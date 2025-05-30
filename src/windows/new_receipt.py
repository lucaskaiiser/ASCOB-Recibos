from .main import tk, ttk
from datetime import datetime

class NewReceiptWindow(tk.Toplevel):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Novo Recibo')
        self.geometry('800x600')
        self.configure(
            background = '#222222',
            padx=20,
            pady=20
        )

        self.form_title = tk.Label(self, text="Novo Recibo")
        self.form_title.grid(row=0, column=0)
        self.create_receipt_form = CreateReceiptForm(self)
        self.create_receipt_form.grid(row=1, column=0, sticky='ns')

        self.actions_form = ActionsCreateReceipt(self)
        self.actions_form.grid(row=3, column=0, )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        

class CreateReceiptForm(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        

        self.inputs = {}

        fields = [
            ("Cliente", "client_name"),
            ("Endereço", "address"),
            ("Valor", "value"),
            ("Por Extenso", "por_extenso"),
            ("Devedor", "debtor_name"),
            ("Número do Boleto", "bill_number"),
            ("Vencimento do Boleto", "bill_due_date"),
            ("Parcela", "installment_number"),
            ("Vencimento da Parcela", "installment_due_date"),
            ("Data do Pagamento", "payment_date"),
            ("Observações", "description"),
            ("Cobrador", "cobrador"),
        ]

        for i, (label_text, field_name) in enumerate(fields):
            label = tk.Label(self, text=label_text)
            label.grid(row=i, column=0, sticky='we')

            entry = tk.Entry(self, width=30)
            entry.grid(row=i, column=1, sticky='w')

            self.inputs[field_name] = entry

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

class ActionsCreateReceipt(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.save_button = tk.Button(self, text='Salvar', command=self.master.destroy)
        self.save_button.grid(row=0, column=0, sticky='e')
        self.cancel_button = tk.Button(self, text='Cancelar', command=self.master.destroy)
        self.cancel_button.grid(row=0, column=1, sticky='w')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)