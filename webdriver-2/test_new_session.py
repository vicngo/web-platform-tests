import features
from utils import assert_resp, feature, TestBase

class Tests(TestBase):
    def test_new_session(self):
        resp = self.force_new_session()
        assert_resp(resp, status=200, keys=[("sessionId", unicode),
                                            ("value", dict)])

    def test_new_session_no_capabilities(self):
        resp = self.force_new_session(raw_body={})
        #XXX Don't know what should happen here really
        assert_resp(resp, status=200, keys=[("sessionId", unicode),
                                            ("value", dict)])

    def test_new_session_empty_body(self):
        resp = self.force_new_session(raw_body="")
        assert_resp(resp, status=500, keys=[("status", unicode)])
        assert resp.data["status"] == "invalid argument"

    def test_new_session_invalid_body_string(self):
        resp = self.force_new_session(raw_body="\"abc\"")
        assert_resp(resp, status=500, keys=[("status", unicode)])
        assert resp.data["status"] == "invalid argument"

    def test_new_session_invalid_body_number(self):
        resp = self.force_new_session(raw_body="123")
        assert_resp(resp, status=500, keys=[("status", unicode)])
        assert resp.data["status"] == "invalid argument"

    def test_new_session_invalid_body_list(self):
        resp = self.force_new_session(raw_body="[[\"capabiltites\", []]]")
        assert_resp(resp, status=500, keys=[("status", unicode)])
        assert resp.data["status"] == "invalid argument"

    @feature(features.MAXIMUM_ONE_SESSION)
    def test_new_session_already_started(self):
        resp = self.force_new_session()
        assert_resp(resp, status=200)
        resp = self.wd.new_session()
        assert_resp(resp, status=500, keys=[("status", unicode)])
        #???
        assert resp.data["status"] == "session not created"
