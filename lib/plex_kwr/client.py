import attr
import requests
from bs4 import BeautifulSoup

# Replace this at some point to use the Python Plex API to obtain the token in the first place

@attr.s
class PlexClient(object):
    url = attr.ib()
    token = attr.ib()