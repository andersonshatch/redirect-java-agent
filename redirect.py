from pathlib import Path
import requests

MAVEN_SEARCH_URL = "https://search.maven.org/solrsearch/select"
MAVEN_SEARCH_PARAMS = {
    "q": "g:com.contrastsecurity a:contrast-agent",
    "wt": "json",
    "core": "gav",
    "rows": "20",
    "start": "0",
}

versions_count = -1
versions = []

while versions_count == -1 or len(versions) < versions_count:
    MAVEN_SEARCH_PARAMS["start"] = str(len(versions))
    print("paging", MAVEN_SEARCH_URL, MAVEN_SEARCH_PARAMS)
    response = requests.get(MAVEN_SEARCH_URL, MAVEN_SEARCH_PARAMS)
    response_json = response.json()
    versions_count = response_json["response"]["numFound"]
    versions.extend(response_json["response"]["docs"])

latest_version = versions[0]["v"]
print(f"got {len(versions)} versions")


def maven_download_url(version: str):
    return f"https://search.maven.org/remotecontent?filepath=com/contrastsecurity/contrast-agent/{version}/contrast-agent-{version}.jar"


latest_version_url = maven_download_url(latest_version)

output_dir = Path("publish")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / Path("_redirects")

lines = []
lines.append(f"latest\t{latest_version_url}")
print(f"selecting latest as {latest_version}")


latest_major_versions = {}

for version_data in versions:
    version = version_data["v"]
    major = version.split(".")[0]
    if major not in latest_major_versions:
        version = version_data["v"]
        latest_major_versions[major] = version
        lines.append(f"{major}\t{maven_download_url(version)}")
        print(f"selecting latest of v{major} as {version}")


output_file.write_text("\n".join(lines))
