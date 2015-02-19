import client
from client import Missing

def assert_equals(actual, expected):
    assert actual == expected, "Expected %r, got %r" % (expected, actual)

def assert_contains(key, collection):
    assert key in collection

def assert_error(resp, code):
    error_codes = {
        "element not selectable": 400,
        "element not visible": 400,
        "invalid argument": 400,
        "invalid cookie domain": 400,
        "invalid element coordinates": 400,
        "invalid element state": 400,
        "invalid selector": 400,
        "invalid session id": 404,
        "javascript error": 500,
        "move target out of bounds": 500,
        "no such alert": 400,
        "no such element": 404,
        "no such frame": 400,
        "no such window": 400,
        "script timeout": 408,
        "session not created": 500,
        "stale element reference": 400,
        "timeout": 408,
        "unable to set cookie": 500,
        "unexpected alert open": 500,
        "unknown error": 500,
        "unknown path": (404, "unknown command"),
        "unknown method": (404, "unknown command"),
        "unsupported operation": 500,
    }
    if code in error_codes:
        expected = error_codes[code]
        if isinstance(expected, tuple):
            http_status, status = expected
        else:
            http_status = expected
            status = code
        assert_equals(resp.status, http_status)
        assert_equals(resp.data.keys(), ["status", "message"])
        assert_equals(resp.data["status"], status)
    else:
        raise ValueError("Unknown error status %s" % status)

def assert_resp(resp, status=None, error=None, keys=None):
    if status is not None:
        assert_equals(resp.status, status)

    if error is not None:
        assert_equals(resp.error, error)

    if keys is not None:
        for key in keys:
            if isinstance(key, (str, unicode)):
                assert_contains(resp["data"], key)
            else:
                name, data_type = key
                assert name in resp.data
                assert isinstance(resp.data[name], data_type)


