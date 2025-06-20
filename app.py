from src.models import start_database_connection
from src.windows import MainWindow
from src.managers.window_manager import WindowManager
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

start_database_connection()

wm = WindowManager()
main_window  = MainWindow(wm)
wm.root = main_window
main_window.mainloop()