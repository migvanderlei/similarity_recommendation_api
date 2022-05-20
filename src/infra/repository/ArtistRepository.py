from src.infra.client.MongoDbClient import MongoDbClient

class ArtistRepository:

    def __init__(self, mongo_db_client: MongoDbClient):
        self.db = mongo_db_client.get_database()
        self.collection = self.db['artists_data']

    def get_all(self):
        return list(self.collection.find())

    def get_by_id(self, id_):
        return self.collection.find_one({"id": id_})

    def get_by_name(self, name):    
        return self.collection.find_one({"name": name})

    def insert_one(self, artist):
        self.collection.insert_one(artist)

    def insert_many(self, artists):
        self.collection.insert_many(artists)
