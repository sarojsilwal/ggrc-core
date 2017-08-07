# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

set -o nounset
set -o errexit

set -x

CURRENT_SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd -P )
$CURRENT_SCRIPTPATH/install_deps.sh

$CURRENT_SCRIPTPATH/../bin/jenkins/run_code_style -p

echo "Testing env variables."
echo $API_VERSION_NUMBER
echo $API_VERSION_NUMBER2
