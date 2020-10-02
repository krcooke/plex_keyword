import attr
import requests
from bs4 import BeautifulSoup

@attr.s
class PlexEPG(object):
    plex_client = attr.ib()

    def refresh_epg(self):

        sections = {'movie': {'section': 1,
                              'type': 1},
                    'episode': {'section': 2,
                                'type': 4}, 
                    'sport': {'section': 3,
                              'type': 4}}



        for media_type in sections.keys():
            epg_url = f'{self.plex_client.url}/tv.plex.providers.epg.onconnect:2/sections/{sections[media_type].section}/all?type={sections[media_type].type}&X-Plex-Product=Plex%20Web&X-Plex-Version=3.67.1&X-Plex-Platform=Firefox&X-Plex-Platform-Version=62.0&X-Plex-Sync-Version=2&X-Plex-Device=Windows&X-Plex-Device-Name=Firefox&X-Plex-Device-Screen-Resolution=1920x966%2C1920x1080&X-Plex-Token={self.plex_client.token}&X-Plex-Language=en&X-Plex-Text-Format=plain'

            res = requests.get(epg_url)

            setattr(self, media_type, BeautifulSoup(res.text,"html.parser"))

    def get_media(self, media_type, keywords):
        """
        Returns a list of media to record based on a list of supplied keywords
        """
        media = getattr(self, media_type, [])

        new_media = []
        for media_item in media.find_all("video"):
            
            # Check the top level elements
            for field in ['summary', 'title']:
                if any(x in media_item[field].lower() for x in keywords):
                    new_media.append(media_item)

            # Check the child tags
            for child_tag in media_item.find_all(["director","writer","role"]):
                if any(x in child_tag['tag'].lower() for x in keywords):
                    new_media.append(media_item)

        return new_media