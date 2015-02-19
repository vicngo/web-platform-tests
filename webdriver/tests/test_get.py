from tools.webdriver import TestBase, test as t

class Test(TestBase):
    def test_get_http(self):
        resp = self.session.get(self.session.url("/"))
        t.assert_resp(resp, status=200)
        t.assert_equals(resp.data, {})

    def test_get_data(self):
        resp = self.session.get("data:test/html,<p>Test")
        t.assert_resp(resp, status=200)
        t.assert_equals(resp.data, {})

    def test_get_image(self):
        resp = self.session.get(self.session.url("/common/green.png"))
        t.assert_resp(resp, status=200)
        t.assert_equals(resp.data, {})

    def test_get_svg(self):
        resp = self.session.get(self.session.url("/common/green.svg"))
        t.assert_resp(resp, status=200)
        t.assert_equals(resp.data, {})

    def test_get_no_url(self):
        t.assert_error(self.session.get(None, raw_body={}), "invalid argument")

