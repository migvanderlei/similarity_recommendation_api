"""
Script to prepare a .tsv file with artists descriptions
"""

from glob import glob
import re

RAW_TEXT_PATH = '/home/miguel/Downloads/dataset-artist-similarity/lastfmapi_biographies'
INDEX_FILE_PATH = '/home/miguel/Downloads/dataset-artist-similarity/mb2uri_lastfmapi.txt'
OUTPUT_FILE_PATH = '/home/miguel/Workspace/similarity_recommendation_api/data/dataset.tsv'

def get_id(filename):
    """ Gets id part from file path """
    filename = filename.rsplit('/', 1)[-1]
    return filename.replace('.txt', '')

def remove_urls(raw_text):
    """ Removes URL-like patterns """
    return re.sub(r'https?://[A-Za-z0-9.?=%/+_-]+', '', raw_text)

def remove_single_characters(raw_text, characters_set):
    """ Removes characters passed by argument as characters_set """
    return ''.join([c for c in raw_text if c not in characters_set])

def remove_empty_parenthesis(raw_text):
    """ Removes trailing empty parenthesis """
    return re.sub(r'\(\)', '', raw_text)

def process_file(filename):
    """ Processes a text file. """
    text = ""

    with open(filename, 'r', encoding='UTF-8') as f:
        text = f.read()

    text = remove_single_characters(text, set(['[', ']', '_', '*']))
    text = remove_urls(text)
    text = remove_empty_parenthesis(text)

    return (get_id(filename), str(text))

def build_artist_index():
    """ Builds an index with id and artist names"""
    index = {}

    with open(INDEX_FILE_PATH, 'r', encoding='UTF-8') as f:
        raw_file = f.read().split('\n')

        for line in raw_file:
            if line:
                identifier, artist_name, artist_url = line.split('\t')

                index[identifier] = {
                    "id": identifier,
                    "name": artist_name.title(),
                    "url": artist_url
                }
    return index

def write_output(output_data):
    """ Writes final output file """
    with open(OUTPUT_FILE_PATH, 'w+', encoding='UTF-8') as f:
        f.write(output_data)

# 20244d07-534f-4eff-b4d4-930878889970 Taylor
files = glob(RAW_TEXT_PATH+'/*.txt')

artist_index = build_artist_index()

data = ['id\tartist_name\turl\ttext']

for file in files:
    artist_id, processed_text = process_file(file)

    artist = artist_index[artist_id]

    data.append(
        f"{artist_id}\t{artist['name']}\t{artist['url']}\t{processed_text}"
    )

write_output("\n".join(data))
