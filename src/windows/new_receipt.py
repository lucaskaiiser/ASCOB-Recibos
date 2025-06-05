from .main import tk, ttk
from tkinter import messagebox
from datetime import datetime

class NewReceiptWindow(tk.Toplevel):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Novo Recibo')
        
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

        self.emission_date = tk.Label(self, text=f'Data de emissão: {datetime.now().date()}')
        self.emission_date.grid(row=2, column=0)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        



class CreateReceiptForm(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

            self.inputs[field_name] = entry

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
    def get_form_values(self):
        values_dict = {
            field_name:entry.get() for field_name,entry in self.inputs.items()
        }
        return(values_dict)

    def create_receipt(self):
        from src.models.receipt import Receipt
        values_dict = self.get_form_values()
        try:
            
            Receipt.create(
                date=datetime.now(),
                **values_dict
                )
            self.master.master.receipts_frame.refresh_tree()
        except Exception as err:
            messagebox.showerror("Erro", err)
            
        finally:
            self.master.destroy()
        



class ActionsCreateReceipt(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.save_button = tk.Button(
            self, text='Salvar',
            command=self.master.create_receipt_form.create_receipt
        )
        self.save_button.grid(row=0, column=0, sticky='e')
        self.cancel_button = tk.Button(self, text='Cancelar', command=self.master.destroy)
        self.cancel_button.grid(row=0, column=1, sticky='w')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)