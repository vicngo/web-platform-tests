import json

import client
import test
from client import Missing

class TestBase(object):
    def __init__(self, config=None):
        if config is None:
            config = self._read_config()
        self.config = config
        self.wd = client.WebDriver(config)

    @property
    def session(self):
        if not self.wd.session:
            self.wd.new_session()
        return self.wd.session

    def force_new_session(self, session_id=Missing, required_capabilities=Missing,
                          desired_capabilites=Missing, raw_body=Missing, headers=Missing):
        if self.wd.session is not None:
            try:
                self.session.end()
            except Exception as e:
                import traceback
                print traceback.format_exc()
        rv = self.wd.new_session(session_id=session_id,
                                 required_capabilities=required_capabilities,
                                 desired_capabilites=desired_capabilites,
                                 raw_body=raw_body,
                                 headers=headers)
        return rv


    def teardown(self):
        if self.wd.session:
            self.session.end()

    def _read_config(self):
        if os.path.exists("config.json"):
            with open("config.json") as f:
                return json.load(f)

        raise IOError("Could not read config.json file")
        

