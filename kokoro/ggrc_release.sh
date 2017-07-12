#!/bin/bash

. /tmpfs/src/gfile/some_config

CURRENT_SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd -P )
$CURRENT_SCRIPTPATH/install_deps.sh

cd "${CURRENT_SCRIPTPATH}/../"
./git_hooks/post-checkout

CONFIG_PREFIX="./extras/deploy/"
PROJECT_NAME="ggrc-sandbox"
CONFIG_DIR="$CONFIG_PREFIX/$PROJECT_NAME/"

mkdir -p "$CONFIG_DIR"

SERVICE_ACCOUNT="$SERVICE_ACCOUNT" #"test-jenkins@ggrc-dev.iam.gserviceaccount.com"
SERVICE_ACCOUNT_FILE="$CONFIG_DIR/service-account"
KEY_FILE="$CONFIG_DIR/$SERVICE_ACCOUNT.key"
SETTINGS_FILE="$CONFIG_DIR/settings.sh"
OVERRIDE_FILE="$CONFIG_DIR/override.sh"

# db_migrate skip
cat >bin/db_migrate <<EOL
#!/usr/bin/env bash
exit 0
EOL

# app.yaml.dist override
cat >src/app.yaml.dist <<EOL
# # Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
#
# See https://developers.google.com/appengine/docs/python/config/appconfig

runtime: python27
api_version: 1
threadsafe: true
instance_class: {INSTANCE_CLASS}
service: test-deployment

{SCALING}

handlers:
{STATIC_SERVING}

  - url: /login
    script: ggrc.app.app.wsgi_app
    login: required
    secure: always

  - url: /_background_tasks/.*
    script: ggrc.app.app.wsgi_app
    login: admin
    secure: always

  - url: /notify_emaildigest
    script: ggrc.app.app.wsgi_app
    login: admin
    secure: always

#  - url: /notify_email_deferred
#    script: ggrc.app.app.wsgi_app
#    login: admin
#    secure: always

  - url: /.*
    script: ggrc.app.app.wsgi_app
    secure: always

libraries:
  - name: MySQLdb
    version: "latest"
  - name: jinja2
    version: "2.6"

builtins:
- remote_api: on

# Don't upload some files
#  - note the first 9 items are defaults, see:
#    https://developers.google.com/appengine/docs/python/config/appconfig#Skipping_Files
skip_files:
- ^(.*/)?app\.yaml
- ^(.*/)?app\.yml
- ^(.*/)?index\.yaml
- ^(.*/)?index\.yml
- ^(.*/)?#.*#
- ^(.*/)?.*~
- ^(.*/)?.*\.py[co]
- ^(.*/)?.*/RCS/.*
- ^(.*/)?\..*
# Custom GGRC excludes here
- requirements\.txt
- requirements\.txt\.md5
- requirements-dev\.txt
- requirements-selenium\.txt
- migrations/.*
- tests/.*
- service_specs/.*
- assets/.*
- reports/.*
- extras/deploy/.*

# Define certain environment variables
env_variables:
  GGRC_SETTINGS_MODULE: "{SETTINGS_MODULE}"
  GGRC_DATABASE_URI: "{DATABASE_URI}"
  GGRC_SECRET_KEY: "{SECRET_KEY}"
  GGRC_GOOGLE_ANALYTICS_ID: "{GOOGLE_ANALYTICS_ID}"
  GGRC_GOOGLE_ANALYTICS_DOMAIN: "{GOOGLE_ANALYTICS_DOMAIN}"
  GGRC_GAPI_KEY: "{GAPI_KEY}"
  GGRC_GAPI_CLIENT_ID: "{GAPI_CLIENT_ID}"
  GGRC_GAPI_CLIENT_SECRET: "{GAPI_CLIENT_SECRET}"
  GGRC_GAPI_ADMIN_GROUP: "{GAPI_ADMIN_GROUP}"
  GGRC_BOOTSTRAP_ADMIN_USERS: "{BOOTSTRAP_ADMIN_USERS}"
  GGRC_MIGRATOR: "{MIGRATOR}"
  GGRC_RISK_ASSESSMENT_URL: "{RISK_ASSESSMENT_URL}"
  APPENGINE_EMAIL: "{APPENGINE_EMAIL}"
  GGRC_CUSTOM_URL_ROOT: "{CUSTOM_URL_ROOT}"
  GGRC_ABOUT_URL: "{ABOUT_URL}"
  GGRC_ABOUT_TEXT: "{ABOUT_TEXT}"
  GGRC_EXTERNAL_HELP_URL: "{EXTERNAL_HELP_URL}"
  MAX_INSTANCES: "{MAX_INSTANCES}"
  AUTHORIZED_DOMAINS: "{AUTHORIZED_DOMAINS}"
  GGRC_Q_INTEGRATION_URL: "{GGRC_Q_INTEGRATION_URL}"
  AUDIT_DASHBOARD_INTEGRATION_URL: "{AUDIT_DASHBOARD_INTEGRATION_URL}"
  ALLOWED_QUERYAPI_APP_IDS: "{ALLOWED_QUERYAPI_APP_IDS}"

EOL

# Custom logging settings
cat >src/ggrc/settings/log.py <<EOL
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
    "ggrc.utils.benchmarks": "DEBUG",
}
EOL

echo $SERVICE_ACCOUNT > "$SERVICE_ACCOUNT_FILE"

# Fill in private.key with the user's private key
cat >"$KEY_FILE" <<EOL
{
  "type": "$ACCOUNT_TYPE",
  "project_id": "$PROJECT_ID",
  "private_key_id": "$PRIVATE_KEY_ID",
  "private_key": "$PRIVATE_KEY",
  "client_email": "$CLIENT_EMAIL",
  "client_id": "$CLIENT_ID",
  "auth_uri": "$AUTH_URI",
  "token_uri": "$TOKEN_URI",
  "auth_provider_x509_cert_url": "$AUTH_PROVIDER_X509_CERT_URL",
  "client_x509_cert_url": "$CLIENT_X509_CERT_URL"
}
EOL


cat >"$SETTINGS_FILE" <<EOL
#!/usr/bin/env bash

APPENGINE_INSTANCE="$APPENGINE_INSTANCE"
SETTINGS_MODULE="$SETTINGS_MODULE"
DATABASE_URI="$DATABASE_URI"
SECRET_KEY="$SECRET_KEY"
GOOGLE_ANALYTICS_ID="$GOOGLE_ANALYTICS_ID"
GOOGLE_ANALYTICS_DOMAIN="$GOOGLE_ANALYTICS_DOMAIN"
GAPI_KEY="$GAPI_KEY"
GAPI_CLIENT_ID="$GAPI_CLIENT_ID"
GAPI_CLIENT_SECRET="$GAPI_CLIENT_SECRET"
GAPI_ADMIN_GROUP="$GAPI_ADMIN_GROUP"
BOOTSTRAP_ADMIN_USERS="$BOOTSTRAP_ADMIN_USERS"
MIGRATOR="$MIGRATOR"
RISK_ASSESSMENT_URL="$RISK_ASSESSMENT_URL"
ABOUT_URL="https://www.google.com"
ABOUT_TEXT="About GGRC"
EXTERNAL_HELP_URL="$EXTERNAL_HELP_URL"
INSTANCE_CLASS="$INSTANCE_CLASS"
MAX_INSTANCES="$MAX_INSTANCES"
CUSTOM_URL_ROOT="$CUSTOM_URL_ROOT"
SCALING="$SCALING"
STATIC_SERVING="$STATIC_SERVING"
GGRC_Q_INTEGRATION_URL="$GGRC_Q_INTEGRATION_URL"
AUDIT_DASHBOARD_INTEGRATION_URL="$AUDIT_DASHBOARD_INTEGRATION_URL"
ALLOWED_QUERYAPI_APP_IDS="$ALLOWED_QUERYAPI_APP_IDS"

# Not present in extras/deploy_settings_local.sh
APPENGINE_EMAIL="$APPENGINE_EMAIL"
AUTHORIZED_DOMAINS=""
EOL

cat >"$OVERRIDE_FILE" <<EOF
#!/usr/bin/env bash

export GGRC_SETTINGS_MODULE="$SETTINGS_MODULE"
export GGRC_DATABASE_URI="$GGRC_DATABASE_URI"
EOF

./bin/deploy ggrc-sandbox
