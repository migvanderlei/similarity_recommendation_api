"""
Script to prepare a .tsv file with artists descriptions
"""
import uuid
from regex import P
from tqdm import tqdm

from retrieve_artist_data import get_image_url, retrieve_artist_data

# RAW_TEXT_PATH = '/home/miguel/Downloads/dataset-artist-similarity/lastfmapi_biographies'
INDEX_FILE_PATH = '/home/miguel/Workspace/similarity_recommendation_api/data/index.txt'
OUTPUT_FILE_PATH = '/home/miguel/Workspace/similarity_recommendation_api/data/new-dataset.tsv'

def write_output(output_data):
    """ Writes final output file """
    with open(OUTPUT_FILE_PATH, 'w+', encoding='UTF-8') as f:
        f.write(output_data)

# # 20244d07-534f-4eff-b4d4-930878889970 Taylor
# files = glob(RAW_TEXT_PATH+'/*.txt')

# artist_index = build_artist_index()

artists = []

with open(INDEX_FILE_PATH, 'r', encoding='UTF-8') as f:
    artists = f.read().split('\n')
    artists = artists[:-1]


data = ['id\tartist_name\tdate_of_birth\torigin\timage_url\ttext']

for artist in tqdm(artists):

    try:
        birthdate, location, text = retrieve_artist_data(artist)
        image_url = get_image_url(artist)
        artist_id = str(uuid.uuid4())

        data.append(
            f"{artist_id}\t{artist}\t{birthdate}\t{location}\t{image_url}\t{text}"
        )
    except KeyboardInterrupt:
        exit()
    except BaseException as e:
        print(artist, e)
        continue

write_output("\n".join(data))
