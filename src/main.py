import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ui.main_app import MAPApp

if __name__ == "__main__":
    app = MAPApp()
    app.run()
