from pathlib import Path
import requests

MAVEN_SEARCH_URL = "https://search.maven.org/solrsearch/select"
MAVEN_SEARCH_PARAMS = [
    ("q", "g:com.contrastsecurity a:contrast-agent"),
    ("wt", "json"),
    ("core", "gav"),
]

response = requests.get(MAVEN_SEARCH_URL, MAVEN_SEARCH_PARAMS)

response_json = response.json()
versions = response_json["response"]["docs"]
latest_version = versions[0]["v"]


def maven_download_url(version: str):
    return f"https://search.maven.org/remotecontent?filepath=com/contrastsecurity/contrast-agent/{version}/contrast-agent-{version}.jar"


latest_version_url = maven_download_url(latest_version)

output_dir = Path("publish")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / Path("_redirects")

lines = []
lines.append(f"latest\t{latest_version_url}")


latest_major_versions = {}

for version_data in versions:
    version = version_data["v"]
    major = version.split(".")[0]
    if major not in latest_major_versions:
        latest_major_versions[major] = version
        lines.append(f"{major}\t{maven_download_url(version)}")


output_file.write_text("\n".join(lines))
