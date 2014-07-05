#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for
from analyzer import how_much

import sys, logging
logging.basicConfig(stream=sys.stderr)

app = Flask(__name__)


@app.route('/')
def form():
    return render_template('base.html')


@app.route('/results/', methods=['POST'])
def results():
    url = request.form["query_url_name"]
    results = how_much.main(url)
    return "<code><pre> %s </pre></code>" % results


if __name__ == "__main__":
    app.run(debug=True)
