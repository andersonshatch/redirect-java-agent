from pathlib import Path
import requests
from requests.adapters import HTTPAdapter, Retry
import json
import os

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

REDIRECT_PREFIX = os.environ.get("REDIRECT_PREFIX", "")

MAVEN_SEARCH_URL = "https://search.maven.org/solrsearch/select"
MAVEN_SEARCH_PARAMS = {
    "q": "g:com.contrastsecurity a:contrast-agent",
    "wt": "json",
    "core": "gav",
    "rows": "20",
    "start": "0",
}

if versions_override := os.environ.get("VERSIONS_OVERRIDE"):
    versions = json.loads(versions_override)
    versions_count = len(versions)
else:
    versions = []
    versions_count = -1


while versions_count == -1 or len(versions) < versions_count:
    MAVEN_SEARCH_PARAMS["start"] = str(len(versions))
    print("paging", MAVEN_SEARCH_URL, MAVEN_SEARCH_PARAMS)
    response = session.get(
        MAVEN_SEARCH_URL,
        params=MAVEN_SEARCH_PARAMS,
        timeout=float(os.environ.get("REQUEST_TIMEOUT", 5)),
    )
    response_json = response.json()
    versions_count = response_json["response"]["numFound"]
    versions.extend((version["v"] for version in response_json["response"]["docs"]))

latest_version = versions[0]
print(f"got {len(versions)} versions")


def maven_download_url(version: str):
    return f"https://search.maven.org/remotecontent?filepath=com/contrastsecurity/contrast-agent/{version}/contrast-agent-{version}.jar"


def route_redirect(version: str, dest: str, status_code: int = 302):
    return {"route": version, "redirect": dest, "statusCode": status_code}


latest_version_url = maven_download_url(latest_version)

output_dir = Path("publish")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / Path("staticwebapp.config.json")
routes = []

routes.append(route_redirect(f"{REDIRECT_PREFIX}latest", latest_version_url))
print(f"selecting latest as {latest_version}")


latest_major_versions = {}

for version_data in versions:
    version = version_data
    major = version.split(".")[0]
    if major not in latest_major_versions:
        version = version_data
        latest_major_versions[major] = version
        routes.append(
            route_redirect(f"{REDIRECT_PREFIX}{major}", maven_download_url(version))
        )
        print(f"selecting latest of v{major} as {version}")


config = {"routes": routes}
output_file.write_text(json.dumps(config))

print("file contents:")
print(output_file.read_text())
