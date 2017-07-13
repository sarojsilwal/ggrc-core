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
