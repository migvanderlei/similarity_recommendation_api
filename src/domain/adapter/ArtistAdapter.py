from src.domain.entity.Artist import Artist

class ArtistAdapter:
    def to_json(self, artist: Artist):
        return {
            "id": artist.id_,
            "name": artist.artist_name,
            "birthDate": artist.date_of_birth,
            "origin": artist.origin,
            "imageUrl": artist.image_url,
            "description": artist.text
        }
        
    def to_json_no_text(self, artist: Artist):
        return {
            "id": artist.id_,
            "name": artist.artist_name,
            "birthDate": artist.date_of_birth,
            "origin": artist.origin,
            "imageUrl": artist.image_url,
        }
        
    def to_json_only_name(self, artist: Artist):
        return {
            "id": artist.id_,
            "name": artist.artist_name
        }

    def to_artist(self, raw_data):
        return Artist(
            raw_data.get('id'), raw_data.get('name'), raw_data.get('description'),
            raw_data.get('imageUrl'), raw_data.get('birthDate'), raw_data.get('origin')
        )