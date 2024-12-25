import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(path)
print(f"Added {path} to sys.path")

from src.ui.main_app import MAPApp

if __name__ == "__main__":
    app = MAPApp()
    app.run()
