# musictag

Tag audio files with correct metadata, utilizing musicbrainz api and beets. Built with flask.

# config.py

Secrets are expected to be found in ```config.py```, which should be placed in the root directory. An example layout is provided below:
```
APPNAME = "Name of App"
CONTACT = "ContactEmailAddr@yourwebsite.com"
```
These are used by the musicbrainz API to handle requests. Further information can be found [here.](https://musicbrainz.org/doc/MusicBrainz_API)