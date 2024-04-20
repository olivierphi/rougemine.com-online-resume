from typing import TYPE_CHECKING, Callable

from .db import clear_cache

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class TOMLCacheClearingMiddleware:
    def __init__(self, get_response: Callable[["HttpRequest"], "HttpResponse"]):
        self.get_response = get_response

    def __call__(self, request: "HttpRequest") -> "HttpResponse":
        # We flush the TOML parsing cache on each request
        clear_cache()

        return self.get_response(request)
