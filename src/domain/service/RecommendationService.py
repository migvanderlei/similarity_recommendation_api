from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from src.domain.adapter.ArtistAdapter import ArtistAdapter

from src.infra.repository.ArtistRepository import ArtistRepository
from src.infra.client.MongoDbClient import MongoDbClient

CURRENT_PATH = str(Path(__file__).resolve().parent)
DATA_PATH = CURRENT_PATH+'/../../../data'
FILENAME = 'cosine_similarity.csv'

class RecommendationService:

    def __init__(self):
        self.repository = ArtistRepository(MongoDbClient())
        self.adapter = ArtistAdapter()


    def load_dataframe(self) -> pd.DataFrame:
        all_data = self.repository.get_all()
        
        all_data = [
            self.adapter.to_json(artist)
            for artist in all_data
        ]
        
        index = [data.get('id') for data in all_data]

        df = pd.DataFrame(all_data, index=index)

        return df

    def get_texts(self, df: pd.DataFrame) -> np.ndarray:
        return np.array(df.description)

    def compute_cosine_similarity(self, embeddings: np.ndarray, index) -> pd.DataFrame:
        cosine_similarity_data = pd.DataFrame(
            cosine_similarity(embeddings)
        )

        cosine_similarity_data = cosine_similarity_data.set_index(index)
        cosine_similarity_data.columns = index.to_list()
        
        cosine_similarity_data.to_csv(DATA_PATH+'/'+FILENAME)

        return cosine_similarity_data
    
    def load_cosine_similarity(self) -> pd.DataFrame:
        cosine_similarity_data = pd.read_csv(DATA_PATH+'/'+FILENAME, index_col=0)

        return cosine_similarity_data

    def recommend(self, index, cosine_similarity_data):
        recommendation = cosine_similarity_data.loc[index].sort_values(ascending=False).index.tolist()[1:6]

        return recommendation
 