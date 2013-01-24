#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.
from moulinrouge import create_app
import logging
app = create_app()

try:
    from log_colorizer import make_colored_stream_handler
    handler = make_colored_stream_handler()
    app.logger.handlers = []
    app.logger.addHandler(handler)
    import werkzeug
    werkzeug._internal._log('debug', '<-- I am with stupid')
    logging.getLogger('werkzeug').handlers = []
    logging.getLogger('werkzeug').addHandler(handler)

    handler.setLevel(logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)
except:
    pass


try:
    import wsreload
except ImportError:
    app.logger.debug('wsreload not found')
else:
    url = "http://moulinrouge.l:21112/*"

    def log(httpserver):
        app.logger.debug('WSReloaded after server restart')
    wsreload.monkey_patch_http_server({'url': url}, callback=log)
    app.logger.debug('HTTPServer monkey patched for url %s' % url)

try:
    import wdb
except ImportError:
    pass
else:
    app.wsgi_app = wdb.Wdb(app.wsgi_app, start_disabled=True)

app.run(debug=True, threaded=True, host='0.0.0.0', port=21112)
