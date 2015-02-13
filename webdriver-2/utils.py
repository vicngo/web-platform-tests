import client
from client import Missing

def assert_resp(resp, status=None, error=None, keys=None):
    if status is not None:
        assert resp.status == status

    if error is not None:
        assert resp.error == error

    if keys is not None:
        for key in keys:
            if isinstance(key, (str, unicode)):
                assert key in resp["data"]
            else:
                name, data_type = key
                assert name in resp.data
                assert isinstance(resp.data[name], data_type)

def close_session(func):
    def inner():
        session = client.Session()
        try:
            func(session)
        finally:
            try:
                session.end()
            except Exception:
                raise
    inner.__name__ = func.__name__
    return inner

class feature(object):
    def __init__(self, *args):
        self.skip = not all(args)

    def __call__(self, func):
        def inner(*args, **kwargs):
            if not self.skip:
                return func(*args, **kwargs)
            else:
                #indicate the test was skipped, somehow
                pass
        inner.__name__ = func.__name__
        return inner

class TestBase(object):
    def __init__(self):
        self.wd = client.WebDriver()

    @property
    def session(self):
        return self.wd.session

    def force_new_session(self, session_id=Missing, required_capabilities=Missing,
                          desired_capabilites=Missing, raw_body=Missing, headers=Missing):
        if self.session is not None:
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
        assert self.session is not None
        return rv

    def teardown(self):
        if self.session:
            self.session.end()
