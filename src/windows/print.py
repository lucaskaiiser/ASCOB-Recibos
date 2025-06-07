from .main import ttk, tk

class ReceiptPrint(tk.Toplevel):
    def __init__(self, receipt_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        