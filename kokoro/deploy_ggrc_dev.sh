#!/bin/bash

echo "Renaming settings"
mv /tmpfs/src/gfile/settings_ggrc_dev /tmpfs/src/gfile/settings

CURRENT_SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd -P )
export ABOUT_TXT='About ggrc dev'
export CURRENT_SCRIPTPATH
$CURRENT_SCRIPTPATH/ggrc_release.sh
