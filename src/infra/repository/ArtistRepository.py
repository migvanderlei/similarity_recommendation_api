from src.domain.adapter.ArtistAdapter import ArtistAdapter
from src.infra.client.MongoDbClient import MongoDbClient

class ArtistRepository:

    def __init__(self, mongo_db_client: MongoDbClient):
        self.db = mongo_db_client.get_database()
        self.collection = self.db['artists_data']
        self.adapter = ArtistAdapter()

    def get_all(self):
        raw_artists = self.collection.find()
        return [
            self.adapter.to_artist(raw_artist)
            for raw_artist in raw_artists
        ]

    def get_by_id(self, id_):
        raw_artist = self.collection.find_one({"id": id_})
        return self.adapter.to_artist(raw_artist)
   
    def get_by_name(self, name):    
        raw_artist = self.collection.find_one({"name": name})
        return self.adapter.to_artist(raw_artist)

    def insert_one(self, artist):
        self.collection.insert_one(artist)

    def insert_many(self, artists):
        self.collection.insert_many(artists)
