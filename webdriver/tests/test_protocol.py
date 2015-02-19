from tools.webdriver import TestBase, test as t

class Test(TestBase):
    def test_wrong_method(self):
        if self.session:
            self.session.end()
        resp = self.wd.send("GET", "/session")
        t.assert_error(resp, "unknown method")

    def test_wrong_path(self):
        resp = self.wd.send("POST", "/sessions", {})
        t.assert_error(resp, "unknown path")

    def test_get_body(self):
        try:
            self.force_new_session()
            resp = self.session.get_title(raw_body={"json": "value"})
            t.assert_resp(resp, status=200, keys=[("value", unicode)])
        finally:
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
            resp = self.session.get_title(raw_body="}{")
            t.assert_resp(resp, status=200, keys=[("value", unicode)])
        finally:
            try:
                self.wd.close_connection()
                self.session.end()
            except Exception:
                pass
