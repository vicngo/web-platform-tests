from tools.webdriver import TestBase, test as t

class Test(TestBase):
    def test_keys(self):
        self.session.get(self.session.url("/webdriver/resources/form.html"))
        resp, elem = self.session.find_element("css selector", "input")
        send_keys_resp = elem.send_keys("PASS")
        t.assert_resp(send_keys_resp, status=200)
        t.assert_equals(send_keys_resp.data, {})
        resp = self.session.execute_script("""return document.querySelector('input').value""");
        t.assert_resp(resp, status=200)
        t.assert_equals(resp.data, {"value": "PASS"})
