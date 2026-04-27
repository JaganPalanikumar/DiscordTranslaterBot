"""Compatibility shim for Python 3.13+ where stdlib cgi was removed.

This project depends on googletrans -> httpx 0.13.x, which still imports
`cgi.parse_header`. We provide just that function for compatibility.
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
