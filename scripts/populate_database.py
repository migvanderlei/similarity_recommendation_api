from pathlib import Path
from src.domain.entity.Artist import Artist
from src.infra.repository.ArtistRepository import ArtistRepository
from src.infra.client.MongoDbClient import MongoDbClient

CURRENT_PATH = str(Path(__file__).resolve().parent)
DATA_PATH = CURRENT_PATH+'/../data'
FILENAME = 'new-dataset.tsv'

tsv_data = []

with open(DATA_PATH+'/'+FILENAME, 'r', encoding='UTF-8') as f:
    tsv_data = f.read().split('\n')

artists = []

for line in tsv_data:
    id_, artist_name, date_of_birth, origin, image_url, text = line.split('\t')

    artists.append(
        Artist(id_, artist_name, text, image_url, date_of_birth, origin).to_json()
    )

db_client = MongoDbClient()
repository = ArtistRepository(db_client)

repository.insert_many(artists)