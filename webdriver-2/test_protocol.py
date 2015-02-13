import client
from utils import assert_resp, TestBase

class Test(TestBase):
    def test_wrong_method(self):
        if self.session:
            self.session.end()
        resp = self.wd.send("GET", "/session")
        assert_resp(resp, status=404, keys=[("status", unicode)])
        assert resp.data["status"] == "unknown command"

    def test_wrong_path(self):
        resp = self.wd.send("POST", "/sessions", {})
        assert_resp(resp, status=404, keys=[("status", unicode)])
        assert resp.data["status"] == "unknown command"

    def test_get_body(self):
        try:
            self.force_new_session()
            print "session", self.session
            resp = self.session.get_title(raw_body={"json": "value"})
            assert_resp(resp, status=200, keys=[("value", unicode)])
        finally:
            # These were tripping over a bug in hyper
            try:
                self.wd.close_connection()
                self.session.end()
            except Exception:
                pass

    def test_get_body_non_json(self):
        try:
            resp = self.force_new_session()
            if resp.error:
                raise Exception(resp)
            print self.session.session_id
            resp = self.session.get_title(raw_body="}{")
            assert_resp(resp, status=200, keys=[("value", unicode)])
        finally:
            try:
                self.wd.close_connection()
                self.session.end()
            except Exception:
                pass
