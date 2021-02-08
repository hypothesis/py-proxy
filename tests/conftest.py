import pytest
from h_matchers import Any


@pytest.fixture
def pyramid_settings():
    return {
        "client_embed_url": "http://hypothes.is/embed.js",
        "nginx_server": "http://via3.hypothes.is",
        "via_html_url": "https://viahtml3.hypothes.is/proxy",
        "checkmate_url": "http://localhost:9099",
        "checkmate_enabled": True,
        "nginx_secure_link_secret": "not_a_secret",
        "via_secret": "not_a_secret",
        "signed_urls_required": True,
    }


def assert_cache_control(headers, cache_parts):
    """Assert that all parts of the Cache-Control header are present."""
    assert dict(headers) == Any.dict.containing({"Cache-Control": Any.string()})
    assert (
        headers["Cache-Control"].split(", ") == Any.list.containing(cache_parts).only()
    )
