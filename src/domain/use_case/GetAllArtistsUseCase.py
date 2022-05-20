from src.domain.adapter.ArtistAdapter import ArtistAdapter
from src.infra.client.MongoDbClient import MongoDbClient
from src.infra.repository.ArtistRepository import ArtistRepository


class GetAllArtistsUseCase:
    def __init__(self):
        mongo_db_client = MongoDbClient()
        self.artist_repository = ArtistRepository(mongo_db_client)
        self.adapter = ArtistAdapter()

    def execute(self):

        artists = self.artist_repository.get_all()

        if artists:
            return [
                    self.adapter.to_json_only_name(artist)
                    for artist in artists
            ]
        return []
