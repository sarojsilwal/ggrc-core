# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Test comment

set -o nounset
set -o errexit

# AppArmor was blocking MySQL to use some of .so libraries and most of kokoro tests were failing. Disabling it solved the problem.
sudo /etc/init.d/apparmor stop
sudo /etc/init.d/apparmor teardown
sudo update-rc.d -f apparmor remove
