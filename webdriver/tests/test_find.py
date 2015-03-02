from tools.webdriver import TestBase, test as t

elem_key = "element-6066-11e4-a52e-4f735466cecf"

class TestFindElement(TestBase):
    def test_find(self):
        self.session.get(self.session.url("/webdriver/resources/element.html"))
        resp, _ = self.session.find_element("css selector", "#a")
        t.assert_resp(resp, 200)
        t.assert_equals(resp.data["value"].keys(), [elem_key])


class TestFindSubelement(TestBase):
    def test_find(self):
        self.session.get(self.session.url("/webdriver/resources/element.html"))
        resp, parent = self.session.find_element("css selector", "#b")
        t.assert_resp(resp, 200)
        resp_test, test = parent.find_element("css selector", ".sub")
        resp_expected, expected = self.session.find_element("css selector", "#ba")
        t.assert_equals(test.id, expected.id)
