def create_app(*args, **kwargs):
    from .interfaces.http.app import create_app as http_create_app

    return http_create_app(*args, **kwargs)


def register_error_handlers(app):
    from .interfaces.http.app import (
        register_error_handlers as http_register_error_handlers,
    )

    return http_register_error_handlers(app)


__all__ = ["create_app", "register_error_handlers"]
