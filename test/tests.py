#!/usr/bin/env python

from moulinrouge import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=21112)
