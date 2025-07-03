import musicbrainzngs
import musicbrainzngs.musicbrainz
from config import APPNAME, CONTACT
import subprocess
import time
from pathlib import Path

print("Agent Load")

UNTAGGED_SONG_PATH = Path('./untagged-music')
TAGGED_SONG_PATH = Path('./tagged-music')
TEMP_SONG_PATH = Path('./tmp')

current_untagged_songs = []

VALID_SONG_FORMATS = ['flac','mp3','aac','wav','aiff','alac','m4a','ogg','opus']

MOCK_DATA = [{'id': 'e15f4b30-a034-4bea-bdd7-d1958278a1bf', 'ext:score': '100', 'title': 'Gnarly', 'status': 'Official', 'text-representation': {'language': 'eng', 'script': 'Latn'}, 'artist-credit': [{'name': 'Oatmeal', 'artist': {'id': 'bd841834-d1b0-494d-adb0-fc5f10979a06', 'name': 'Oatmeal', 'sort-name': 'Oatmeal'}}], 'release-group': {'id': 'f62634d5-21c4-4a71-b3d7-ce8b14bff1c6', 'type': 'Single', 'title': 'Gnarly', 'primary-type': 'Single'}, 'date': '2020-01-31', 'country': 'US', 'release-event-list': [{'date': '2020-01-31', 'area': {'id': '489ce91b-6658-3307-9877-795b68554c98', 'name': 'United States', 'sort-name': 'United States', 'iso-3166-1-code-list': ['US']}}], 'asin': 'B0844Q9NGX', 'medium-list': [{'format': 'Digital Media', 'disc-list': [], 'disc-count': 0, 'track-list': [], 'track-count': 1}], 'medium-track-count': 1, 'medium-count': 1, 'tag-list': [], 'artist-credit-phrase': 'Oatmeal'}, {'id': '37347c11-dd53-4d52-aade-078ddb7c32f3', 'ext:score': '100', 'title': 'Gnarly', 'status': 'Official', 'disambiguation': 'clean', 'packaging': 'None', 'text-representation': {'language': 'eng', 'script': 'Latn'}, 'artist-credit': [{'name': 'KATSEYE', 'artist': {'id': 'abbf7d85-9a7f-4a6c-80bd-bf71f2c7d520', 'name': 'KATSEYE', 'sort-name': 'KATSEYE'}}], 'release-group': {'id': '60e4cc5b-cf97-4dae-b0c1-d30adb8c11cc', 'type': 'Single', 'title': 'Gnarly', 'primary-type': 'Single'}, 'barcode': '00602478028991', 'label-info-list': [{'label': {'id': '5ab1234e-05c3-4260-8b00-a208224dd96b', 'name': 'HYBE × GEFFEN'}}], 'medium-list': [{'format': 'Digital Media', 'disc-list': [], 'disc-count': 0, 'track-list': [], 'track-count': 1}], 'medium-track-count': 1, 'medium-count': 1, 'tag-list': [], 'artist-credit-phrase': 'KATSEYE'}]
MOCK_IMAGE_DATA = {'images': [{'approved': True, 'back': False, 'comment': '', 'edit': 127293211, 'front': True, 'id': 42166269002, 'image': 'https://coverartarchive.org/release/37347c11-dd53-4d52-aade-078ddb7c32f3/42166269002.jpg', 'thumbnails': {'1200': 'https://coverartarchive.org/release/37347c11-dd53-4d52-aade-078ddb7c32f3/42166269002-1200.jpg', '250': 'https://coverartarchive.org/release/37347c11-dd53-4d52-aade-078ddb7c32f3/42166269002-250.jpg', '500': 'https://coverartarchive.org/release/37347c11-dd53-4d52-aade-078ddb7c32f3/42166269002-500.jpg', 'large': 'https://coverartarchive.org/release/37347c11-dd53-4d52-aade-078ddb7c32f3/42166269002-500.jpg', 'small': 'https://coverartarchive.org/release/37347c11-dd53-4d52-aade-078ddb7c32f3/42166269002-250.jpg'}, 'types': ['Front']}], 'release': 'https://musicbrainz.org/release/37347c11-dd53-4d52-aade-078ddb7c32f3'}
musicbrainzngs.set_useragent(APPNAME,"1.0.0",CONTACT)

print("set agent name")

# result = musicbrainzngs.search_artists(artist="iroha") # type="group", country="GB"
# for artist in result['artist-list']:
#     print(u"{id}: {name}".format(id=artist['id'], name=artist["name"]))

print("query loaded:")

# result = musicbrainzngs.search_releases("Gnarly",limit=1) # type="group", country="GB"
# for release in result['release-list']:
#     print(u"{name}, {artist} ({id})".format(name=release["title"],artist=release['artist-credit']['name'],id=release['id']))
# print(result)

def find_by_song(title):
    fullList = []
    print("Looking for:", title)
    if str.strip(title) == '':
        print("bad")
        return None
    result = musicbrainzngs.search_releases(str.strip(title),limit=7) # type="group", country="GB"
    for release in result['release-list']:
        artistList = []
        for obj in release['artist-credit']:
            try:
                artistList.append(obj['name'])
            except:
                artistList.append("Unknown")
        cover =  MOCK_IMAGE_DATA #musicbrainzngs.get_image_list(release['id'])
        item = {}
        item['name']=release["title"]
        item['artist']=artistList
        item['id']=release['id']
        item['cover']=cover['images'][0]['thumbnails']['small']
        fullList.append(item)
        print("=========")
    return fullList

def get_cover(mbid):
    print("looking for cover for id",mbid)
    try:
        x = musicbrainzngs.get_image_list(mbid)
    except musicbrainzngs.musicbrainz.ResponseError:
        return "{{ url_for('static', filename='placeholder_cover.png') }}"
    return x['images'][0]['thumbnails']['small']

def apply_metadata(mbid):
    # print(musicbrainzngs.search_recordings(query="炉心融解"))
    process = subprocess.Popen(['beet','-l','./library.db','-d','./tagged-music','import','--search-id',mbid,'./tmp'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    process.stdin.write('A')
    while not process.stdout.readline():
        time.sleep(0.1)
    print(process.communicate()[0])



def get_local_songs():
    print("refreshing current local songs...")
    current_untagged_songs = []
    print("local songs are:")
    for file in UNTAGGED_SONG_PATH.iterdir():
        # TODO: Use regex or equiv to make this cleaner
        if file.is_file() and (file.name[-4:] in VALID_SONG_FORMATS or file.name[-3:] in VALID_SONG_FORMATS):
            print(file)
            current_untagged_songs.append(file.name)
    return current_untagged_songs

def move_current_song(file: Path):
    try:
        # Ensure the parent directory of the destination exists
        TEMP_SONG_PATH.mkdir(parents=True, exist_ok=True)
        # Move the file
        file.rename(TEMP_SONG_PATH.joinpath(file.name).resolve())
        print(f"File '{file.name}' moved successfully to '{TEMP_SONG_PATH.name}'.")
    except FileNotFoundError:
        print(f"Error: Source file '{file}' not found.")
    except OSError as e:
        print(f"Error moving file: {e}")

if __name__ == "__main__":
    print("loaded")

    get_local_songs()


