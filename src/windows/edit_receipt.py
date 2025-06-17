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
        self.form_title.grid(row=0, column=0,sticky='w',pady=10)
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

    def edit_receipt(self):
        old_data = self.edit_receipt_form.old_data
        new_data = self.edit_receipt_form.get_form_values()
        try:
            for item, value in new_data.items():
                if value == '':
                    raise ValueError(f'Há campos não preenchidos')
                    
                new_data[item] = value.strip()
        
        except ValueError as err:
            messagebox.showerror(message=err)
            return

        try:
            new_data['date'] = datetime.strptime(new_data['date'], '%d/%m/%Y').date()
        except ValueError:
            messagebox.showerror(message='Insira a data no formato dia/mês/ano')
            return

        try:
            new_data['value'] = round(float(new_data['value']),2)
        except ValueError as err:
            messagebox.showerror(message='O campo "Valor" deve ser no formato real.centavo')
            return
        except Exception as err:
            messagebox.showerror(message=str(err))
            return
        if old_data != new_data:
            confirmation = messagebox.askyesno(
                title='Confirmar Alteração nos dados do recibo',
                message=f'Deseja aplicar as alterações no recibo {self.receipt_data['id']}?'
            )
            if confirmation:
                self.wm.controller.edit_receipt(self.receipt_data['id'], new_data)
                self.wm.root.receipts_frame.refresh_tree()
                self.destroy()
            return
        messagebox.showinfo(
            message='Sem alterações para aplicar'
        )
        
        
class EditReceiptForm(ttk.Frame):
    def __init__(self, master, receipt_data, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.inputs = {}

        fields = [
            ("Cliente", "client_name"),
            ("Devedor", "debtor"),
            ("Endereço", "address"),
            ("Valor", "value"),
            #("Por Extenso", "por_extenso"),
            #("Número do Boleto", "bill_number"),
            #("Vencimento do Boleto", "bill_due_date"),
            #("Parcela", "installment_number"),
            #("Vencimento da Parcela", "installment_due_date"),
            #("Data do Pagamento", "payment_date"),
            #("Observações", "description"),
            ("Cobrador", "cobrador"),
        ]

        for i, (label_text, field_name) in enumerate(fields):
            label = ttk.Label(self, text=label_text)
            label.grid(row=i, column=0, sticky='we', padx=10)

            entry = ttk.Entry(self, width=40)
            entry.grid(row=i, column=1, sticky='w', pady=5)
            print(receipt_data[field_name])
            self.inputs[field_name] = entry.insert(0,receipt_data[field_name] or '')

            self.inputs.update(
                {field_name: entry }
            )

        
        label = ttk.Label(self, text='Descrição')
        label.grid(row=len(fields), column=0, sticky='nw', padx=10)
        entry = tk.Text(self, width=27, height=10, font=("Arial", 8))
        entry.grid(row=len(fields), column=1, sticky='wnes', pady=5)
        entry.insert("1.0", receipt_data['description'] or '')
        self.inputs.update(
                {'description': entry}
            )

        label = ttk.Label(self, text='Data Emissão')
        label.grid(row=len(fields)+1, column=0, sticky='nw', padx=10, pady=10)
        entry_date = ttk.Entry(self, width=40)
        entry_date.grid(row=len(fields)+1, column=1, sticky='wnes', pady=10)
        entry_date.insert(0,receipt_data['date'].strftime('%d/%m/%Y'))

        self.inputs['date'] = entry_date
        
        ### Text "Referente A" Limitation
        def limitar_texto(event):
            MAX_CHARS = 255
            conteudo = self.inputs['description'].get("1.0", "end-1c")
            if len(conteudo) >= MAX_CHARS and event.keysym != 'BackSpace':
                return "break"
        
        self.inputs['description'].bind("<Key>", limitar_texto)
        ###

        self.old_data = self.get_form_values()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def get_form_values(self):
        values_dict = {
            field_name:entry.get() for field_name,entry in self.inputs.items() if field_name != 'description'
        }
        values_dict.update({
            'description': self.inputs['description'].get("1.0", "end-1c")
        })
        return values_dict

class ActionsEditReceipt(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.edit_button = ttk.Button(self, text='Editar', command=self.master.edit_receipt)
        self.edit_button.grid(row=0, column=0, sticky='w', padx=10)
        #self.edit_button['state'] = 'disabled'

        self.exclude_button = ttk.Button(self, text='Excluir', command=self.master.delete_receipt)
        self.exclude_button.grid(row=0, column=0, sticky='e', padx=10)

        self.exit_button = ttk.Button(self, text='Sair', command=self.master.destroy)
        self.exit_button.grid(row=0, column=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)