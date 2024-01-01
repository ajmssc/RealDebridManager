from realdebridmanager.rd.api.api import WithRDAPIInterface


class WithUserAPI(WithRDAPIInterface):

    def get_user(self):
        return self._get('/user')
