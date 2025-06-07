from .main import tk, ttk
from tkinter import messagebox
from datetime import datetime

class NewReceiptWindow(tk.Toplevel):
    def __init__(self,wm,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm = wm
        self.title('Novo Recibo')
        
        self.configure(
            background='#F5F6F7',
            padx=20,
            pady=20
        )

        self.form_title = ttk.Label(
            self,
            text="Novo Recibo",
            font=('Red Hat Display', 16)
            
        )
        self.form_title.grid(row=0, column=0, sticky='w')
        self.create_receipt_form = CreateReceiptForm(master=self, wm=self.wm)
        self.create_receipt_form.grid(row=1, column=0, sticky='ns', pady=20)

        self.actions_form = ActionsCreateReceipt(master =self, wm=self.wm)
        self.actions_form.grid(row=3, column=0 )

        self.emission_date = ttk.Label(
            self,
            text=f'Data de emissão: {datetime.now().date().strftime('%d/%m/%Y')}')
        self.emission_date.grid(row=2, column=0, sticky='w', pady=20)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
class CreateReceiptForm(ttk.Frame):
    def __init__(self,wm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm = wm
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
            ("Cobrador", "cobrador"),
            ("Observações", "description"),
        ]

        for i, (label_text, field_name) in enumerate(fields):
            label = ttk.Label(self, text=label_text)
            if field_name == 'description':
                label.grid(row=i, column=0, sticky='wen', padx=10)
                entry = tk.Text(self, width=30, height=10)
            else:
                label.grid(row=i, column=0, sticky='we', padx=10)
                entry = ttk.Entry(self, width=30)
            entry.grid(row=i, column=1, sticky='w', pady=5)

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
            
            receipt = Receipt.create(
                date=datetime.now(),
                **values_dict
                )
            self.master.master.receipts_frame.refresh_tree()
            self.wm.root.receipts_frame.tree.selection_set(receipt.id)
            self.wm.root.receipts_frame.tree.focus(receipt.id)

        except Exception as err:
            messagebox.showerror(title="Erro",message= err)
            
        finally:
            self.master.destroy()
            

class ActionsCreateReceipt(ttk.Frame):
    def __init__(self, wm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm =wm
        self.save_button = ttk.Button(
            self, text='Salvar',
            command=self.master.create_receipt_form.create_receipt
        )
        self.save_button.grid(row=0, column=0, sticky='e')
        self.cancel_button = ttk.Button(self, text='Cancelar', command=self.master.destroy)
        self.cancel_button.grid(row=0, column=1, sticky='w')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)