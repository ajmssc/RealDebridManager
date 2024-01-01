
from realdebridmanager.rd.api.api import WithRDAPIInterface


class WithStreamingAPI(WithRDAPIInterface):

    def get_streaming_transcode(self, download_id):
        return self._get('/streaming/transcode/' + download_id)

    def get_streaming_media_info(self, download_id):
        return self._get('/streaming/mediaInfo/' + download_id)
