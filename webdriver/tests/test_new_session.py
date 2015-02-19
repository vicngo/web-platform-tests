from tools.webdriver import TestBase, test as t

class Tests(TestBase):
    def test_new_session(self):
        resp = self.force_new_session()
        t.assert_resp(resp, status=200, keys=[("sessionId", unicode),
                                            ("value", dict)])

    def test_new_session_no_capabilities(self):
        resp = self.force_new_session(raw_body={})
        #XXX Don't know what should happen here really
        t.assert_resp(resp, status=200, keys=[("sessionId", unicode),
                                            ("value", dict)])

    def test_new_session_empty_body(self):
        resp = self.force_new_session(raw_body="")
        t.assert_error(resp, "invalid argument")

    def test_new_session_invalid_body_string(self):
        resp = self.force_new_session(raw_body="\"abc\"")
        t.assert_error(resp, "invalid argument")

    def test_new_session_invalid_body_number(self):
        resp = self.force_new_session(raw_body="123")
        t.assert_error(resp, "invalid argument")

    def test_new_session_invalid_body_list(self):
        resp = self.force_new_session(raw_body="[[\"capabiltites\", []]]")
        t.assert_error(resp, "invalid argument")

#    @feature(features.MAXIMUM_ONE_SESSION)
    def test_new_session_already_started(self):
        resp = self.force_new_session()
        t.assert_resp(resp, status=200)
        resp = self.wd.new_session()
        t.assert_resp(resp, status=500, keys=[("status", unicode)])
        #???
        t.assert_error(resp, "session not created")
