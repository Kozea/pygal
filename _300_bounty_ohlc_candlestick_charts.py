import logging

from moulinrouge import create_app

app = create_app()

try:
    from log_colorizer import make_colored_stream_handler
    handler = make_colored_stream_handler()
    app.logger.handlers = []
    app.logger.addHandler(handler)
    import werkzeug
    werkzeug._internal._log('debug', '<-- I am with stupid')
    logging.getLogger('werkzeug').handlers = []
    logging.getLogger('werkzeug')..