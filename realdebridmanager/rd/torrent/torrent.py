from typing import List

from realdebridmanager.rd.api.api import WithRDAPIInterface


class WithTorrentAPI(WithRDAPIInterface):

    def get_torrents(self):
        return self._get('/torrents')

    def get_torrent_info(self, torrent_id):
        return self._get('/torrents/info/' + torrent_id)

    def get_torrent_instant_availability(self, torrent_hash):
        return self._get(f'/torrents/instantAvailability/{torrent_hash}')

    def get_torrent_active_count(self):
        return self._get('/torrents/activeCount')

    def get_torrent_available_hosts(self):
        return self._get('/torrents/availableHosts')

    def add_torrent(self, torrent_data):
        return self._put('/torrents/addTorrent', data=torrent_data)

    def add_torrent_magnet(self, magnet_link):
        return self._post('/torrents/addMagnet', data={"magnet": magnet_link})

    def select_files(self, torrent_id, files: List[str]):
        return self._post('/torrents/selectFiles/' + torrent_id, data={"files": ','.join(files)}, json=False)

    def delete_torrent(self, torrent_id):
        return self._delete('/torrents/delete/' + torrent_id, json=False)