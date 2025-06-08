import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(base_dir, 'runtime')
os.environ['PATH'] = dll_path + os.pathsep + os.environ['PATH']

from src.models import start_database_connection
from src.windows import MainWindow
from src.managers.window_manager import WindowManager

start_database_connection()

wm = WindowManager()
main_window  = MainWindow(wm)
wm.root = main_window
main_window.mainloop()