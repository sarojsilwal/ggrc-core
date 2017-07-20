# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""`appengine_config.py` is automatically loaded when Google App Engine starts
a new instance of your application. This runs before any WSGI applications
specified in app.yaml are loaded.
"""

import os

from google.appengine.ext import vendor

# Third-party libraries are stored in "packages", vendoring will make
# sure that they are importable by the application.
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PACKAGES_PATH = os.path.join(DIR_PATH, "packages")
vendor.add(PACKAGES_PATH)
