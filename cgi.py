# Needed because Python 3.13+ removed stdlib cgi, but googletrans/httpx still imports cgi.parse_header.
"""Compatibility shim for Python 3.13+ where stdlib cgi was removed.

CGI means Common Gateway Interface, an older web standard for how web servers
talk to scripts. A header is HTTP metadata (for example, Content-Type).
`cgi.parse_header` splits a header value into the main type and its parameters,
such as "text/plain; charset=utf-8" -> ("text/plain", {"charset": "utf-8"}).

This project depends on googletrans -> httpx 0.13.x, which still imports
`cgi.parse_header`, so we provide just that function for compatibility.
"""

from email.message import Message


def parse_header(line):
    """Parse a Content-Type style header into (value, params)."""
    if line is None:
        return "", {}

    msg = Message()
    msg["content-type"] = line
    value = msg.get_content_type()
    params = dict(msg.get_params()[1:] or [])
    return value, params
