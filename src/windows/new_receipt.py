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
        self.create_receipt_form.grid(row=1, column=0, sticky='ns', pady=10)

        self.actions_form = ActionsCreateReceipt(master =self, wm=self.wm)
        self.actions_form.grid(row=3, column=0 )
        
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
            #("Por Extenso", "por_extenso"),
            ("Devedor", "debtor"),
            ("Endereço", "address"),
            ("Valor", "value"),
            #("Número do Boleto", "bill_number"),
            #("Vencimento do Boleto", "bill_due_date"),
            #("Parcela", "installment_number"),
            #("Vencimento da Parcela", "installment_due_date"),
            #("Data do Pagamento", "payment_date"),
            ("Cobrador", "cobrador"),
            #("Observações", "description"),
            
        ]

        for i, (label_text, field_name) in enumerate(fields):
            label = ttk.Label(self, text=label_text)
            label.grid(row=i, column=0, sticky='we', padx=10)
            entry = ttk.Entry(self, width=40)
            entry.grid(row=i, column=1, sticky='w', pady=5)

            self.inputs[field_name] = entry

        label = ttk.Label(self, text='Descrição')
        label.grid(row=len(fields), column=0, sticky='nw', padx=10, pady=10)
        entry = tk.Text(self, width=27, height=10, font=("Arial", 8))
        entry.grid(row=len(fields), column=1, sticky='wnes', pady=10)

        self.inputs['description'] = entry

        label = ttk.Label(self, text='Data Emissão')
        label.grid(row=len(fields)+1, column=0, sticky='nw', padx=10, pady=10)
        entry_date = ttk.Entry(self, width=40)
        entry_date.grid(row=len(fields)+1, column=1, sticky='wnes', pady=10)
        entry_date.insert(0,datetime.now().date().strftime('%d/%m/%Y'))

        self.inputs['date'] = entry_date

        ### Text "Referente A" Limitation
        def limitar_texto(event):
            MAX_CHARS = 255
            conteudo = self.inputs['description'].get("1.0", "end-1c")
            if len(conteudo) >= MAX_CHARS and event.keysym != 'BackSpace':
                return "break"
        
        self.inputs['description'].bind("<Key>", limitar_texto)
        ###

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        
    def get_form_values(self):
        values_dict = {
            field_name:entry.get() for field_name,entry in self.inputs.items() if field_name != 'description'
        }
        values_dict.update({
            'description': self.inputs['description'].get("1.0", "end-1c")
        })
        return(values_dict)

    def create_receipt(self):
        from src.models.receipt import Receipt
        values_dict = self.get_form_values()
        try:
            for item, value in values_dict.items():
                if value == '':
                    raise ValueError(f'Há campos não preenchidos')
                    
                values_dict[item] = value.strip()
        
        except ValueError as err:
            messagebox.showerror(message=err)
            return

        print('aaaaa', values_dict)

        try:
            values_dict['value'] = round(float(values_dict['value']),2)

        except ValueError as err:
            messagebox.showerror(message='Valor deve ser no formato real.centavo')
            return
        except Exception as err:
            messagebox.showerror(message=str(err))
            return

        try:
            values_dict['date'] = datetime.strptime(values_dict['date'], '%d/%m/%Y').date()
        except ValueError:
            messagebox.showerror(message='Insira a data no formato dia/mês/ano')
            return 

        try:
            
            receipt = Receipt.create(
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