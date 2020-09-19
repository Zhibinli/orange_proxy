import re
from urllib.parse import parse_qsl, urlparse, urlunparse
from flask import Flask, request, abort, Response, redirect
import requests
import logging

app = Flask("__name__")
logging.basicConfig(level=logging.DEBUG)
CHUNK_SIZE = 1024
LOG = logging.getLogger("app.py")


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def set_header():
    headers = {
        'X-Forwarded-For': "113.198.69.0",
        'X-Msisdn': "+14125006666"
    }
    return headers


@app.route('/')
def root():
    query = urlparse(request.full_path).query
    query_components = dict(parse_qsl(query))
    next = query_components.get('n', None)
    LOG.debug("next param: %s", next)
    if (next is not None):
        enriched_headers = merge_two_dicts(dict(request.headers), set_header())
        r = make_request(
            next,
            request.method,
            enriched_headers,
            request.form
        )
        LOG.critical("response:  %s", r)
        LOG.critical("enriched headers: %s", enriched_headers)

        if (r.status_code == 302):
            LOG.critical("redirect")
            redirect(r.headers['Location'])

        def generate():
            for chunk in r.raw.stream(decode_content=False):
                yield chunk
        out = Response(generate(), headers=dict(r.headers))
        out.status_code = r.status_code
        LOG.critical("out: %s", out)
        return out
    return "Missing next param url 'n'"


def make_request(url, method, headers={}, data=None):
    # Fetch the URL, and stream it back
    LOG.debug("make_request")
    LOG.debug("Sending %s %s with headers: %s and data %s", method, url, headers, data)
    resp = requests.request(
        method,
        url,
        params=request.args,
        stream=True,
        headers=headers,
        allow_redirects=False,
        data=data
    )
    return resp


if __name__ == "__main__":
    app.run()
