# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

set -o nounset

clean_project_name () {
  # Clean the project name of characters other than [A-Za-z0-9]
  echo "${1:-}" | sed 's/[^A-Za-z0-9]//g'
}
