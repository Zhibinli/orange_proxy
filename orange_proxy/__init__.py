import re
from urllib.parse import parse_qsl, urlparse, urlunparse
from flask import Flask, request, abort, Response, redirect
import requests
import logging

app = Flask("__name__")
logging.basicConfig(level=logging.DEBUG)
CHUNK_SIZE = 1024
LOG = logging.getLogger("app.py")


@app.route('/')
def root():
    next = get_next_url()
    if (next is not None):
        enriched_headers = get_enrich_headers()
        enriched_headers.pop('Host')
        r = make_request(
            next,
            request.method,
            enriched_headers,
        )

        def generate():
            for chunk in r.raw.stream(decode_content=False):
                yield chunk
        response = Response(generate(), headers=dict(r.headers))
        response.status_code = r.status_code
        LOG.critical("response: %s\n", response)

        return response
    return "Missing next param url 'n'"


def make_request(url, method, headers={}):
    LOG.debug("making request...")
    LOG.debug("Sending %s %s with headers: %s\n", method, url, headers)
    resp = requests.request(
        method,
        url,
        params=request.args,
        stream=True,
        headers=headers,
        allow_redirects=False,
    )
    return resp


def get_enrich_headers():
    inject = {
        'X-Forwarded-For': "113.198.69.0",
        'X-Msisdn': "+14125006666"
    }
    enriched = dict(request.headers).copy()
    enriched.update(inject)
    LOG.debug("enriched headers: %s\n", enriched)
    return enriched


def get_next_url():
    query = urlparse(request.full_path).query
    query_components = dict(parse_qsl(query))
    next = query_components.get('n', None)
    LOG.debug("next param: %s", next)
    return next

if __name__ == "__main__":
    app.run()
