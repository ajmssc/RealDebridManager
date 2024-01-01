import json
import os

from realdebridmanager.rd.api.api import WithRDAPI
from realdebridmanager.rd.downloads.downloads import WithDownloadsAPI
from realdebridmanager.rd.settings.settings import WithSettingsAPI
from realdebridmanager.rd.streaming.streaming import WithStreamingAPI
from realdebridmanager.rd.time.time import WithTimeAPI
from realdebridmanager.rd.torrent.torrent import WithTorrentAPI
from realdebridmanager.rd.user.user import WithUserAPI


class RealDebrid(WithRDAPI, WithUserAPI, WithTimeAPI, WithTorrentAPI,
                 WithSettingsAPI, WithStreamingAPI, WithDownloadsAPI):

    def __init__(self, api_token):
        super().__init__(api_token)

    def get_user(self):
        return self._get('/user')


if __name__ == '__main__':
    client = RealDebrid(api_token=os.getenv('API_TOKEN'))
    # print(client.get_user())
    # print(client.get_time_iso())
    # import requests
    # torrent_file_url = "https://webtorrent.io/torrents/big-buck-bunny.torrent"
    # torrent_file = requests.get(torrent_file_url)
    # print(client.add_torrent(torrent_file.content))
    # print(len(client.get_torrents()))
    # print(client.get_torrent_info("QASW6IY6NPG3M"))
    # print(client.select_files("QASW6IY6NPG3M", ["all"]))
    # print(client.delete_torrent("QASW6IY6NPG3M"))
    print(json.dumps(client.get_downloads(), indent=4))
