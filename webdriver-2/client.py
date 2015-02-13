import httplib
import json
import urlparse

Missing = object()

class WebDriver(object):
    session = None

    def __init__(self, host=None, port=None, url_prefix="/"):
        #TODO: this is temporary
        if host is None:
            host = "localhost"
        if port is None:
            port = 4444

        self.host = host
        self.port = port
        self.url_prefix = url_prefix
        self._connection = None

    def connect(self):
        self._connection = httplib.HTTPConnection(self.host, self.port)

    def close_connection(self):
        if self._connection:
            self._connection.close()
        self._connection = None

    def send(self, method, url, body=Missing, headers=Missing):
        if not self._connection:
            self.connect()

        if isinstance(body, dict):
            body = json.dumps(body)

        if isinstance(body, unicode):
            body = body.encode("utf-8")

        if body is Missing:
            body = ""

        if self.url_prefix is not Missing:
            url = urlparse.urljoin(self.url_prefix, url)

        if headers is Missing:
            headers = {}

        self._connection.request(method, url, body, headers)

        resp = self._connection.getresponse()

        rv = Response(resp.status, resp.reason, resp.getheaders(), resp.read())

        if not rv.error:
            if url.endswith("/session") and method == "POST" and "sessionId" in rv.data:
                WebDriver.session = Session(self, rv.data["sessionId"])
            elif url.endswith("/session/%s" % self.session.session_id) and method == "DELETE":
                WebDriver.session = None
                self.close_connection()

        return rv

    def new_session(self, session_id=Missing, required_capabilities=Missing,
                    desired_capabilites=Missing, raw_body=Missing, headers=Missing):
        if raw_body is not Missing:
            body = raw_body
        else:
            body = {"capabilities": {"desiredCapabilites":{}}}
            if session_id is not Missing:
                body["sessionId"] = session_id
            if desired_capabilites is not Missing:
                body["desired_capabilites"] = desired_capabilites
            if required_capabilities is not Missing:
                body["required_capabilities"] = required_capabilities

        rv = self.send("POST", "session", body, headers)
        return rv

    def end_session(self, session_id, raw_body=Missing, headers=Missing):
        url = urlparse.urljoin("session/%s", session_id)
        return self.send("DELETE", url, raw_body, headers)

class Session(object):
    def __init__(self, client=None, session_id=None):
        self.session_id = session_id
        if client is None:
            client = WebDriver()
        self.client = client

    def start(self, **kwargs):
        resp = self.client.new_session(**kwargs)
        if not resp.error:
            self.session_id = resp.data["sessionId"]
        return resp

    def end(self, **kwargs):
        if self.session_id:
            resp = self.client.end_session(self.session_id, **kwargs)
            if not resp.error:
                self.session_id = None
            return resp

    def __enter__(self):
        resp = self.start()
        if resp.error:
            raise Exception(resp)
        return self

    def __exit__(self, *args, **kwargs):
        resp = self.end()
        if resp.error:
            raise Exception(resp)

    def send_command(self, method, url, body=Missing, headers=Missing):
        assert self.session_id is not None
        url = urlparse.urljoin("session/%s/" % self.session_id, url)
        return self.client.send(method, url, body, headers)

    def get(self, url, raw_body=Missing, headers=Missing):
        if raw_body is not Missing:
            body = raw_body
        else:
            body = {"url": url}
        return self.send_command("POST", "url", body, headers)

    def get_current_url(self, raw_body=Missing, headers=Missing):
        return self.send_command("GET", "url", raw_body, headers)

    def go_back(self, raw_body=Missing, headers=Missing):
        return self.send_command("POST", "back", raw_body, headers)

    def go_forward(self, raw_body=Missing, headers=Missing):
        return self.send_command("POST", "forward", raw_body, headers)

    def refresh(self, raw_body=Missing, headers=Missing):
        return self.send_command("POST", "refresh", raw_body, headers)

    def get_title(self, raw_body=Missing, headers=Missing):
        return self.send_command("GET", "title", raw_body, headers)

    def get_window_handle(self, raw_body=Missing, headers=Missing):
        return self.send_command("GET", "window_handle", raw_body, headers)

    def get_window_handles(self, raw_body=Missing, headers=Missing):
        return self.send_command("GET", "window_handles", raw_body, headers)

    def close(self, raw_body=Missing, headers=Missing):
        return self.send_command("DELETE", "window_handle", raw_body, headers)

    def set_window_size(self, height, width, raw_body=Missing, headers=Missing):
        if self.raw_body is Missing:
            body = {"width": width,
                    "height": height}
        else:
            body = raw_body
        return self.send_command("POST", "window/size", raw_body, headers)

    def get_window_size(self, raw_body=Missing, headers=Missing):
        return self.send_command("GET", "window/size", raw_body, headers)

    def maximize_window(self, raw_body=Missing, headers=Missing):
        return self.send_command("POST", "window/maximize", raw_body, headers)

    # TODO: not properly defined
    # def fullscreen_window(self, raw_body=Missing, headers=Missing):
    #     return self.send_command("POST", "", raw_body, headers)

class Response(object):
    def __init__(self, status, reason, headers, body):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.raw_body = body

        if body:
            self.data = json.loads(body)
        else:
            self.data = None

        self.error = status != 200


    def __repr__(self):
        return "<Response %s %s>" % (self.status, self.raw_body)
