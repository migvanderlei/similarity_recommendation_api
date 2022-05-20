from pymongo import MongoClient

CONNECTION_STRING = 'mongodb+srv://{}:{}@cluster0.g8kvq.mongodb.net/?retryWrites=true&w=majority'

class MongoDbClient:

    def __init__(self):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        self.connection_string = CONNECTION_STRING.format('migvanderlei', 'U3iKBnMF6ml3IalY')

    def get_database(self, database_name='recommendation'):
        client = MongoClient(self.connection_string)
        return client[database_name]
