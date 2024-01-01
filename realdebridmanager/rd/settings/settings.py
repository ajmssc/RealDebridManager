from typing import Literal

from realdebridmanager.rd.api.api import WithRDAPIInterface


class WithSettingsAPI(WithRDAPIInterface):

    def get_settings(self):
        return self._get('/settings')

    def update_setting(self,
                       setting: Literal["download_port", "locale",
                       "streaming_language_preference", "streaming_quality",
                       "mobile_streaming_quality", "streaming_cast_audio_preference"], value):
        return self._post('/settings/update', data={
            "setting_name": setting,
            "setting_value": value
        }, json=False)
