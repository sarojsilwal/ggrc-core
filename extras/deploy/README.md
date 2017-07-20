# Deployment settings directory

The directory structure:

```
.
├── ggrc-dev
│   ├── service-account
│   ├── test-jenkins@ggrc-dev.iam.gserviceaccount.com.key
│   ├── override.sh
│   └── settings.sh
├── another-project
│   ├── service-account
│   ├── somebody@someproject.iam.gserviceaccount.com.key
│   ├── override.sh
│   └── settings.sh
├── settings-template.sh
├── override-template.sh
└── README.md
```

"ggrc-dev" or "another-project" is used as a parameter to ``./bin/deploy``

"service-account" contains the email of the service-account to perform the deployment, like "test-jenkins@ggrc-dev.iam.gserviceaccount.com".

"*.key" file (the filename can be generated in bash by "$(< service-account).key") is JSON file with private key for the service account.

"override.sh" is a config featuring ``GGRC_DATABASE_URL`` compatible with ``db_migrate``.

"settings.sh" contains settings to be passed to app.yaml.

"settings-template.sh" contains the template for user's "settings.sh".

"override-template.sh" contains the template for user's "override.sh".

## Step-by-step setup

From the project directory, please run:

``` bash
PROJECT="set-your-project-here"
mkdir -pv "./extras/deploy/$PROJECT"
cp "./extras/deploy/override-template.sh" "./extras/deploy/$PROJECT/override.sh"
cp "./extras/deploy/settings-template.sh" "./extras/deploy/$PROJECT/settings.sh"
```

### Fill in override and settings files

TBD

"override.sh" should contain DB connection string with connection by IP as Google Cloud-specific format isn't compatible with the DB migration script.

### Register the service account

TBD

Assuming the JSON private key is ~/Downloads/some-key.json:

``` bash
PROJECT="set-your-project-here"
ACCOUNT="set-service-account-email-here"
echo $ACCOUNT > "./extras/deploy/$PROJECT/service-account"
mv "~/Downloads/some-key.json" "./extras/deploy/$PROJECT/$ACCOUNT.key"
```
