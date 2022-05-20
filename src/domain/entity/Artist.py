class Artist:
    def __init__(self,
        id_=None, artist_name=None, text=None, image_url = None,
        date_of_birth=None, origin = None):

        self.id_ = id_
        self.artist_name = artist_name
        self.image_url = image_url
        self.text = text
        self.date_of_birth = None if date_of_birth == 'None' else date_of_birth
        self.origin = None if origin == 'None' else origin
