# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

echo "MySQL service status"
sudo service mysql status

sudo /etc/init.d/apparmor stop
sudo /etc/init.d/apparmor teardown
sudo update-rc.d -f apparmor remove
