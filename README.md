# Redirect to Contrast Java Agent

Utility script to update Azure Static Web App site redirects to the very latest and latest major versions of `com.contrastsecurity:contrast-agent` on Maven Central.

Files in the `publish` directory are made available on the deployed site.

## Requirements

- Python 3.11 or newer

## Usage

### Inputs

The script reads in an environment variable `NEW_VERSION_URL`.
The value of this environment variable should be the full URL to the download of that version of contrast-agent, e.g. https://repo1.maven.org/maven2/com/contrastsecurity/contrast-agent/5.1.2/contrast-agent-5.1.2.jar

The version is extracted from the first path segment containing a version string; in the above example, from `/5.1.2/`.
This version is checked against existing redirects to versions in `staticwebapp.config.json`.
If a redirect is already present for major version 5, that destination is replaced with the new URL. Else, a new major version redirect will be added to the list.
If the major version to be updated is the current latest major version, or a new major version, the `latest` redirect destination will also be updated to the new URL.


### GitHub Action

The GitHub Action workflow `main.yml` takes in a `new_version_url` input from either manual trigger (via GitHub UI/API), or via repository_dispatch event from another repository.
This version input is used to update the redirects in `staticwebapp.config.json`, and a PR is then opened so the changes can be reviewed. When the PR is merged, the deployment is triggered.

### Local testing / development

1. `pip install -r requirements.txt`
1. `NEW_VERSION_URL=https://new-version-url/111.222.333/contrast-agent-111.222.333.jar python redirect.py`
