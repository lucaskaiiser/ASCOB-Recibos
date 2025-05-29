from .main import tk, ttk

class NewReceiptWindow(tk.Toplevel):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Novo Recibo')
        self.geometry('800x600')
        self.label = tk.Label(
            self, text='Janela de criar Recibo'
        )
        self.label.place(relx=0.1)
        
class CreateReceiptForm(tk.Frame):
    pass

class ActionsCreateReceipt(tk.Frame):
    pass

