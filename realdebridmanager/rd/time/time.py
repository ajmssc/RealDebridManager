from realdebridmanager.rd.api.api import WithRDAPIInterface


class WithTimeAPI(WithRDAPIInterface):

    def get_time(self):
        return self._get('/time', json=False)

    def get_time_iso(self):
        return self._get('/time/iso', json=False)
