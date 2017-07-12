#!/bin/bash

. /tmpfs/src/gfile/some_config

CURRENT_SCRIPTPATH=$( cd "$(dirname "$0")" ; pwd -P )
$CURRENT_SCRIPTPATH/install_deps.sh

cd "${CURRENT_SCRIPTPATH}/../"
./git_hooks/post-checkout

CONFIG_PREFIX="./extras/deploy/"
PROJECT_NAME="ggrc-dev"
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
  "type": "service_account",
  "project_id": "ggrc-dev",
  "private_key_id": "6602e194b425b0954a5f0434b30ef6d60dc90a54",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDr2CracbgrRTts\nwbrVELWm1MXG11gZYoYtXdglCoyYfHohkNRZ5F1DbYY5xyTCzWL5WvSJemquCQtS\ndkxJzVwcpyM1YAPCIUSFn4DEWctVhSArmUfI7V1N5PFZmZOcdYTBRPv16JsebzHz\nBXe1lIv1fWsEL5Ue1wSvkEgT0QSGPObbSUJWmdkOVp24l+S2JCth+ttZht29PYJE\nqBM5zIWrO32L42j63d1b+lKVTNJQL/XA16Nw6rwFE6ez9JHImDsuAAeTQ0+1Ze0S\n7wEpwkr754OsMcpl8JrxU2Z+lhAxYCRF8ZeM+kfWR1JZlkT4/jLi7Fu4cGvH7NJg\n9kR4UqhBAgMBAAECggEBANmI1NYSKF55CDvjYVIfjH2qKhajEFaxwrNbqP9ZgJ8x\nyXDmZofXlJKaFkF6xxSLXyxC0eVwra+DFhdkmC9GpRykqVwVCMJp7wsVOS9i56Ml\nHKw6QLU7A2HSty7+8eFRoDaoS4LhnxpuU/MlaupobsPrf+cngHMmvuK0wVbN509s\nXeobycD8LOhDl9WLZ6oFJrLH4m39st105OJC+/QyjeMzaMTEsXKRsGv5Fde3xDPn\n5LsVjrk3mmIE/bcinmdwueVR1sBS4bkUAg+GFfuKBLTZZ7WN92qvhuISTEsrjy/6\nJAkNDhk4a5gS9EIyNqG86Mg6X+V9ZoE9J/5Jd/bOIVUCgYEA+VJWxb6wf7203wJ6\n8GRBUDveyC9Skhhc9n3cFN3vIZWVhZm7MNZnEHsWtYvFoDb/Wt6KV9o6CBjy+mYK\ndmVMpIBSxMsbnvYgjmZ3vz+463M0COU1BT0dfi6BOK4ol34F9oCYu8L0srgQi7kj\nPs4wVDgQBHoiEwkFdANWp43LeIMCgYEA8ilpY3BJAB/hgrSXe+jFR7m2iC+rzHIn\n5k+pz+vsfhWIX+nvYGYkykEUhzYDkZtgd0wu/ZgT837ELGzQ0DztBBSRD1ODPwNJ\nKwJMuTX3KWhHFC0+ApOY2ocYKiP1eefBI7MFoMG005gyJDO+dUwhkmYwntlSYfMp\nG24YeDgKWOsCgYEAqL41xHifdJWtCRLgqjrwiaE70zlUJVUf9iSRA/6BjrVzEY1O\nyGsULm9gm1cSVrFietoLwBIPHNPl/9t4UVGWYfAIFPFyrE/hEQABJAu42IKMQUkA\nbZ9Ditdm1jnpdz7wQjofJVV50EwLxsVzOVrMEvQuwxj2XvPIIRDxYU3y3IkCgYEA\nmFISF1k+odRr3fJIQsmEpfwb44fQ0XWQwV6kmsN0a06SDHqydnlpdMsA5ZfFIOaS\nBBgoip0JF6VKMgN0STe5glKJeBF4wb8IXARDTFC0mhgcdYWLtsUuZW6KdZ9OvhJX\nu2PVC2wsmNfn2jut9kwf5d1fgduC5Ve1KKrUu3HMmGcCgYBwmTZLuEaRIF9hMyBF\nqF5yhaQ+jo3H5O1mAwgHqoBedbD/Tse56uzeSOQixVRfZxhGDB8B5iaBTm6tBKVo\nUjO2SEpIQWmqMFKdFJDF1hcUj/paMie8JqK00RbVZVG1XjdpzRz1+hHpVPf4lWXL\nTv5F/57RQtvnHfh5l9AREkczRQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "test-jenkins@ggrc-dev.iam.gserviceaccount.com",
  "client_id": "117820491369318290632",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test-jenkins%40ggrc-dev.iam.gserviceaccount.com"
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
EOL

cat >"$OVERRIDE_FILE" <<EOF
#!/usr/bin/env bash

export GGRC_SETTINGS_MODULE="$SETTINGS_MODULE"
export GGRC_DATABASE_URI="$GGRC_DATABASE_URI"
EOF

./bin/deploy ggrc-sandbox
