# Copyright 2019 Jarek Zgoda. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from werkzeug.routing import Map


class Application:

    def __init__(self):
        self.url_map = Map()
        self.endpoints = {}
