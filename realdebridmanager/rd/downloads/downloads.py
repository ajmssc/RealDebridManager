from realdebridmanager.rd.api.api import WithRDAPIInterface


class WithDownloadsAPI(WithRDAPIInterface):

    def get_downloads(self):
        return self._get('/downloads')
