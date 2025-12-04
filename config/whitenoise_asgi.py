from django.conf import settings
from django.contrib.staticfiles import finders
from whitenoise import WhiteNoise
from asgiref.wsgi import WsgiToAsgi
from urllib.parse import urlparse
import os

class WhiteNoiseASGI:
    """
    ASGI wrapper for WhiteNoise to avoid synchronous iterator warnings and blocking the event loop.
    Replicates the configuration logic of WhiteNoiseMiddleware.
    """
    def __init__(self, application):
        self.application = application

        # Calculate configuration based on settings, similar to WhiteNoiseMiddleware
        try:
            autorefresh = settings.WHITENOISE_AUTOREFRESH
        except AttributeError:
            autorefresh = settings.DEBUG

        try:
            max_age = settings.WHITENOISE_MAX_AGE
        except AttributeError:
            if settings.DEBUG:
                max_age = 0
            else:
                max_age = 60

        try:
            allow_all_origins = settings.WHITENOISE_ALLOW_ALL_ORIGINS
        except AttributeError:
            allow_all_origins = True

        try:
            charset = settings.WHITENOISE_CHARSET
        except AttributeError:
            charset = "utf-8"

        try:
            mimetypes = settings.WHITENOISE_MIMETYPES
        except AttributeError:
            mimetypes = None

        try:
            add_headers_function = settings.WHITENOISE_ADD_HEADERS_FUNCTION
        except AttributeError:
            add_headers_function = None

        try:
            index_file = settings.WHITENOISE_INDEX_FILE
        except AttributeError:
            index_file = None

        try:
            immutable_file_test = settings.WHITENOISE_IMMUTABLE_FILE_TEST
        except AttributeError:
            immutable_file_test = None

        # Initialize WhiteNoise with a dummy application
        # (This dummy app should never be called if our check logic is correct)
        def dummy_app(environ, start_response):
            start_response('404 Not Found', [])
            return []

        self.wn = WhiteNoise(
            application=dummy_app,
            autorefresh=autorefresh,
            max_age=max_age,
            allow_all_origins=allow_all_origins,
            charset=charset,
            mimetypes=mimetypes,
            add_headers_function=add_headers_function,
            index_file=index_file,
            immutable_file_test=immutable_file_test,
        )

        # Configure files
        try:
            use_finders = settings.WHITENOISE_USE_FINDERS
        except AttributeError:
            use_finders = settings.DEBUG

        try:
            self.static_prefix = settings.WHITENOISE_STATIC_PREFIX
        except AttributeError:
            self.static_prefix = urlparse(settings.STATIC_URL or "").path
            if settings.FORCE_SCRIPT_NAME:
                script_name = settings.FORCE_SCRIPT_NAME.rstrip("/")
                if self.static_prefix.startswith(script_name):
                    self.static_prefix = self.static_prefix[len(script_name) :]

        # Ensure trailing slash
        if not self.static_prefix.endswith("/"):
            self.static_prefix += "/"

        self.static_root = settings.STATIC_ROOT
        if self.static_root:
            self.wn.add_files(self.static_root, prefix=self.static_prefix)

        try:
            root = settings.WHITENOISE_ROOT
        except AttributeError:
            root = None
        if root:
            self.wn.add_files(root)

        if use_finders and not self.wn.autorefresh:
            self.add_files_from_finders()

        # Wrap with WsgiToAsgi to run in threadpool
        self.wn_asgi = WsgiToAsgi(self.wn)

    def add_files_from_finders(self):
        # Copied/Adapted from WhiteNoiseMiddleware
        files = {}
        for finder in finders.get_finders():
            for path, storage in finder.list(None):
                prefix = (getattr(storage, "prefix", None) or "").strip("/")
                url = "".join(
                    (
                        self.static_prefix,
                        prefix,
                        "/" if prefix else "",
                        path.replace("\\", "/"),
                    )
                )
                files.setdefault(url, storage.path(path))
        stat_cache = {path: os.stat(path) for path in files.values()}
        for url, path in files.items():
            self.wn.add_file_to_dictionary(url, path, stat_cache=stat_cache)

    async def __call__(self, scope, receive, send):
        # Only handle http requests that match the static prefix
        if scope['type'] == 'http':
            path = scope['path']
            if self.should_handle(path):
                await self.wn_asgi(scope, receive, send)
                return

        await self.application(scope, receive, send)

    def should_handle(self, path):
        if self.wn.autorefresh:
            return self.wn.find_file(path) is not None
        else:
            return self.wn.files.get(path) is not None
