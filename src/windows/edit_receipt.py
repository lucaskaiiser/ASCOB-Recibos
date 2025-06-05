from .main import tk, ttk
from datetime import datetime

class EditReceiptWindow(tk.Toplevel):
    def __init__(self, receipt_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Editar Recibo')
        self.receipt_data= receipt_data
        print(receipt_data)
        self.configure(
            background = '#222222',
            padx=20,
            pady=20
        )

        self.form_title = tk.Label(self, text="Editar Recibo")
        self.form_title.grid(row=0, column=0)
        self.edit_receipt_form = EditReceiptForm(self, receipt_data)
        self.edit_receipt_form.grid(row=1, column=0, sticky='ns')

        self.actions_form = ActionsEditReceipt(self)
        self.actions_form.grid(row=2, column=0, )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
 
        

class EditReceiptForm(tk.Frame):
    def __init__(self, master, receipt_data, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.inputs = {}

        fields = [
            ("Cliente", "client_name"),
            ("Endereço", "address"),
            ("Valor", "value"),
            ("Por Extenso", "por_extenso"),
            ("Devedor", "debtor"),
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
            print(receipt_data[field_name])
            self.inputs[field_name] = entry.insert(0,receipt_data[field_name] or '')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

class ActionsEditReceipt(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.edit_button = tk.Button(self, text='Editar', command=self.master.destroy)
        self.edit_button.grid(row=0, column=0, sticky='e')

        self.exit_button = tk.Button(self, text='Sair', command=self.master.destroy)
        self.exit_button.grid(row=0, column=1, sticky='w')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)