# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Log settings that will be used for deployment."""

SQLALCHEMY_RECORD_QUERIES = 'slow'
LOGGING_LOGGERS = {
    "ggrc": "INFO",
    "sqlalchemy": "WARNING",
    # WARNING - logs warnings and errors only
    # INFO    - logs SQL-queries
    # DEBUG   - logs SQL-queries + result sets
    "werkzeug": "INFO",
    # WARNING - logs warnings and errors only
    # INFO    - logs HTTP-queries
    "ggrc.utils.benchmarks": "DEBUG"
}
