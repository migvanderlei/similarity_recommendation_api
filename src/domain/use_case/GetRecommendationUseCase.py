from src.domain.adapter.ArtistAdapter import ArtistAdapter
from src.domain.service.EmbeddingService import EmbeddingService
from src.domain.service.RecommendationService import RecommendationService
from src.infra.client.MongoDbClient import MongoDbClient
from src.infra.repository.ArtistRepository import ArtistRepository


class GetRecommendationUseCase:
    def __init__(self):
        mongo_db_client = MongoDbClient()
        self.artist_repository = ArtistRepository(mongo_db_client)
        self.embedding_service = EmbeddingService()
        self.recommendation_service = RecommendationService()
        self.adapter = ArtistAdapter()

    def execute(self, artist_id):
        data = None
        embeddings = self.embedding_service.load_embeddings()

        if embeddings is None:
            data = self.recommendation_service.load_dataframe()
            texts = self.recommendation_service.get_texts(data)

            embeddings = self.embedding_service.build_embeddings(texts)

        cosine_similarity_data = self.recommendation_service.load_cosine_similarity()

        if cosine_similarity_data is None:
            cosine_similarity_data = self.recommendation_service.compute_cosine_similarity(
                embeddings, data.index
            )

        try:
            recommendations_ids = self.recommendation_service.recommend(
                artist_id,
                cosine_similarity_data
            )

            return self.__resolve_recommendations(recommendations_ids)
        except BaseException:
            return []

    def __resolve_recommendations(self, recommendations_ids):
        return [
            self.adapter.to_json_no_text(
                self.artist_repository.get_by_id(artist_id)
            )
            for artist_id in recommendations_ids
        ]
