import attr
import requests
from bs4 import BeautifulSoup

VIDEO_ATTRS = {'tv': ["grandparentGuid",
                        "grandparentThumb",
                        "grandparentTitle",
                        "grandparentYear",
                        "guid",
                        "index",
                        "originallyavailableat",
                        "originallyAvailableAt",
                        "parentIndex",
                        "title",
                        "type",
                        "year",
                        "airingchannels"],
                'movie': ["guid",
                        "title",
                        "thumb",
                        "year"]
              }

@attr.s
class PlexDVR(object):
    plex_client = attr.ib()
    target_id = attr.ib(kw_only=True)

    media_provider_id = attr.ib(kw_only=True)
    schedule_defaults = attr.ib(kw_only=True)
    no_exec = attr.ib(default=True, kw_only=True)
        
    def __attrs_post_init__(self):
        try:
            res = requests.get(f'{self.plex_client.url}/media/subscriptions?X-Plex-Product=Plex%20Web&X-Plex-Version=3.67.1&X-Plex-Platform=Firefox&X-Plex-Platform-Version=61.0&X-Plex-Sync-Version=2&X-Plex-Device=Windows&X-Plex-Device-Name=Firefox&X-Plex-Device-Screen-Resolution=1920x929%2C1920x1080&X-Plex-Token={self.plex_client.token}&X-Plex-Language=en')
        except Exception as error:
            print(str(error))

        self.scheduled_recordings = BeautifulSoup(res.text,"html.parser")
    
    #target
    def _generate_record_url(self, video):
        #Create the recording
        record_url = f'{self.plex_url}{self.schedule_defaults}'
        record_url += f'&targetLibrarySectionID={self.target_id}'

        for attr in getattr(VIDEO_ATTRS, video.type):
            if video.has_attr(attr):
                value = self.video[attr]
                record_url += f'"&hints[{attr}]=+urllib.parse.quote_plus({value})'

        record_url += f'&params[libraryType]=2&type=4&params[mediaProviderID]={self.media_provider_id}'
        
        return record_url

    def record(self, video):
        record_url = self._generate_record_url(video)
        if self.no_exec:
            print(record_url)

        else:
            res = requests.post(record_url)
            if res.status_code == 200:
                print("Recording successfully created")
                return True
            else:
                print("Error Returned : "+res.status_code)
                return False

    # does the recording already exist?
    def check_schedule(self, video):
        #check to see if this episode or film is already scheduled.
        guid = video.guid
        matchItem = self.scheduled_recordings.select_one(f'video[guid="{guid}"]')
        if matchItem:
            return True
        else:
            return False
