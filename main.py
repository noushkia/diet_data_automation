import os
import sys
from main_page import gui

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    # Ensure the database directory exists relative to where the EXE is run
    if not os.path.exists('db/patients'):
        try:
            os.makedirs('db/patients', exist_ok=True)
        except Exception:
            pass
            
    gui.main()
