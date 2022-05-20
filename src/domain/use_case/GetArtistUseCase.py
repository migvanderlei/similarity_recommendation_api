from src.domain.adapter.ArtistAdapter import ArtistAdapter
from src.infra.client.MongoDbClient import MongoDbClient
from src.infra.repository.ArtistRepository import ArtistRepository


class GetArtistUseCase:
    def __init__(self):
        mongo_db_client = MongoDbClient()
        self.artist_repository = ArtistRepository(mongo_db_client)
        self.adapter = ArtistAdapter()

    def execute(self, artist_id, description=False):
        

        artist = self.artist_repository.get_by_id(artist_id)

        if artist:
            if description:
                return self.adapter.to_json(artist)

            return self.adapter.to_json_no_text(artist)
        return None