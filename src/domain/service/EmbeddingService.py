from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

CURRENT_PATH = str(Path(__file__).resolve().parent)
DATA_PATH = CURRENT_PATH+'/../../../data'
FILENAME = 'embeddings-mpnet.npy'

class EmbeddingService():
    def __init__(self, lazy_setup=True, model_name='all-mpnet-base-v2'):
        self.lazy_setup = lazy_setup
        self.model_name = model_name

        if not lazy_setup:
            self.setup()

    def setup(self):
        self.model = SentenceTransformer(self.model_name)

    def build_embeddings(self, X):
        print("Encoding process started")

        if self.lazy_setup:
            self.setup()

        embeddings = self.model.encode(X)
        np.save(DATA_PATH+'/'+FILENAME, embeddings)

        return embeddings

    def load_embeddings(self):
        try:
            return np.load(DATA_PATH+'/'+FILENAME)
        except FileNotFoundError:
            return None
