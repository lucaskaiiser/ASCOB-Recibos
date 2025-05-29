from .main import tk, ttk

class SearchReceiptWindow(tk.Toplevel):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Buscar Recibo')
        self.geometry('800x600')
        self.label = tk.Label(
            self, text='Janela de Buscar Recibo'
        )
        self.label.place(relx=0.1)

class SearchReceiptForm(tk.Frame):
    pass

class ActionsSearchReceipt(tk.Frame):
    pass

