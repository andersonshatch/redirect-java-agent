from pathlib import Path
import requests

MAVEN_SEARCH_URL="https://search.maven.org/solrsearch/select"
MAVEN_SEARCH_PARAMS=[("q", "g:com.contrastsecurity a:contrast-agent"), ("wt", "json"), ("core", "gav")]

response = requests.get(MAVEN_SEARCH_URL, MAVEN_SEARCH_PARAMS)

latest_version = response.json()['response']['docs'][0]['v']

def maven_download_url(version: str):
    return f"https://search.maven.org/remotecontent?filepath=com/contrastsecurity/contrast-agent/{version}/contrast-agent-{version}.jar"

latest_version_url = maven_download_url(latest_version)

output_dir = Path('publish')
output_dir.mkdir(exist_ok=True)
output_file = output_dir / Path('_redirects')
output_file.write_text(f"latest\t{latest_version_url}")