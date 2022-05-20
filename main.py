""" Main app container"""
import os
from src.app import app

HOST = "0.0.0.0"
PORT = 5000

# Gets the app from app.py and runs it
if __name__ == '__main__':

    port = int(os.environ.get("PORT", PORT))
    app.run(host=HOST, port=port)
