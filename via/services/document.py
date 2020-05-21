import requests
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response

from via.services.timeit import timeit


class Document:
    def __init__(self, document_url):
        self.url = document_url
        self.original = None
        self.content = None

    def get_original(self, headers, expect_type=None):
        user_agent = headers.get("User-Agent")

        print("Requesting URL:", self.url, headers)

        with timeit("retrieve content"):
            original = requests.get(
                self.url,
                # Pass the user agent
                headers={"User-Agent": user_agent},
            )

        print("GOT COOKIES", original.cookies)

        if expect_type:
            content_type = original.headers["Content-Type"]
            if not content_type or expect_type not in content_type:
                raise HTTPNotFound(f"No content of type '{expect_type}' found")

        self.original = original
        self.content = original.content

    def response(self):
        # TODO! Pyramid response construction here seems messy. Maybe we could
        # just return a dict of the right keys, or is that just dodging the
        # issue?

        response = Response(
            body=self.content, content_type=self.original.headers["Content-Type"]
        )

        return response