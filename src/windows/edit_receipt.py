from .main import tk, ttk
from tkinter import messagebox
from datetime import datetime

class EditReceiptWindow(tk.Toplevel):
    def __init__(self, receipt_data,wm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm = wm
        self.title('Editar Recibo')
        self.receipt_data= receipt_data
        print(receipt_data)
        self.configure(
            background='#f5f6f7',
            padx=20,
            pady=20
        )

        self.form_title = ttk.Label(self, text="Editar Recibo",  font=('Red Hat Display', 16))
        self.form_title.grid(row=0, column=0,sticky='w',pady=20)
        self.edit_receipt_form = EditReceiptForm(self, receipt_data)
        self.edit_receipt_form.grid(row=1, column=0, sticky='ns', padx=10)

        self.actions_form = ActionsEditReceipt(self)
        self.actions_form.grid(row=2, column=0,pady=20, sticky='nwse' )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
    
    def delete_receipt(self):
        receipt_id = self.receipt_data['id']
        confirmation = messagebox.askyesno(
            title='Excluir recibo',
            message=('Tem certeza que deseja excluir'+
                f' o recibo {receipt_id} de'+
                f' {self.receipt_data['client_name']}?'
            )
        )
        if confirmation:
            self.wm.controller.delete_receipt(receipt_id)

            self.destroy()
            self.wm.root.receipts_frame.refresh_tree()
            try:
                self.master.search()
            except Exception as err:
                print(err)
        
class EditReceiptForm(ttk.Frame):
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
            label = ttk.Label(self, text=label_text)
            label.grid(row=i, column=0, sticky='we')

            entry = ttk.Entry(self, width=30)
            entry.grid(row=i, column=1, sticky='w')
            print(receipt_data[field_name])
            self.inputs[field_name] = entry.insert(0,receipt_data[field_name] or '')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

class ActionsEditReceipt(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.edit_button = ttk.Button(self, text='Editar', command=self.master.destroy)
        self.edit_button.grid(row=0, column=0, sticky='w', padx=10)

        self.exclude_button = ttk.Button(self, text='Excluir', command=self.master.delete_receipt)
        self.exclude_button.grid(row=0, column=0, sticky='e', padx=10)

        self.exit_button = ttk.Button(self, text='Sair', command=self.master.destroy)
        self.exit_button.grid(row=0, column=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)