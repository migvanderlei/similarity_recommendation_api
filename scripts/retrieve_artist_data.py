import re
import requests
from bs4 import BeautifulSoup

MONTH = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
}

LAST_FM_BASE_URL = "https://www.last.fm{}"
LAST_FM_WIKI_URL = "https://www.last.fm/music/{}/+wiki"
LAST_FM_WIKI_CLASS = "wiki-container"
LAST_FM_WIKI_TEXT_CLASS = "wiki-content"
LAST_FM_WIKI_FACTS_CLASS = "factbox"

LAST_FM_IMAGES_URL = "https://www.last.fm/music/{}/+images"
LAST_FM_IMAGE_ITEM = "image-list-item"
LAST_FM_FULL_IMAGE = "js-gallery-image"

def parse_birthdate(raw_birthdate):
    if raw_birthdate:

        day, written_month, year = re.findall(r'(\d\d?) (\w+) (\d{4})', raw_birthdate)[0]

        day = "0"+day if len(day) == 1 else day 

        return f"{day}/{MONTH[written_month]}/{year}"
    return None

def get_image_url(artist):
    URL = LAST_FM_IMAGES_URL.format("+".join(artist.title().split(' ')))

    first_page = requests.get(URL)

    soup = BeautifulSoup(first_page.content, "html.parser")

    image_link = soup.find("a", class_=LAST_FM_IMAGE_ITEM, href=True)

    image_page = requests.get(LAST_FM_BASE_URL.format(image_link['href']))

    soup = BeautifulSoup(image_page.content, "html.parser")

    image = soup.find("img", class_=LAST_FM_FULL_IMAGE)

    return image['src']

def retrieve_artist_data(artist):

    URL = LAST_FM_WIKI_URL.format("+".join(artist.title().split(' ')))

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    wiki_div = soup.find("div", class_=LAST_FM_WIKI_CLASS)

    raw_text = wiki_div.find("div", class_=LAST_FM_WIKI_TEXT_CLASS).get_text()

    text = re.sub(r'\n', '', raw_text)
    text = re.sub(r'\t', ' ', text)

    factbox = wiki_div.find("ul", class_=LAST_FM_WIKI_FACTS_CLASS)

    if not factbox:
        return (None, None, text)

    facts = factbox.find_all("p")

    if "Members" in factbox.get_text() or "Years Active" in factbox.get_text():

        if len(facts) > 2:
            return (None, facts[1].get_text(), text)
        else:
            return (None, None, text)

    return (parse_birthdate(facts[0].get_text()), facts[1].get_text(), text)

# ARTIST = 'MC Kevin o Chris'

# raw_birthdate, raw_location, raw_text = retrieve_artist_data(ARTIST)
# # image_url = get_image_url(ARTIST)

# # print(raw_text, raw_birthdate, raw_location, image_url)
# print(raw_text, raw_birthdate, raw_location)
