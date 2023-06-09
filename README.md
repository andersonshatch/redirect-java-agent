# Redirect to Contrast Java Agent

Utility script to query Maven Central for versions of `com.contrastsecurity:contrast-agent`, generating a `_redirects` file to the latest of all versions, plus latest of major versions. 

The generated `_redirects` file is supported by Netlify, Cloudflare Pages, and probably others.

## Example output

```
latest	https://search.maven.org/remotecontent?filepath=com/contrastsecurity/contrast-agent/5.1.0/contrast-agent-5.1.0.jar
5	https://search.maven.org/remotecontent?filepath=com/contrastsecurity/contrast-agent/5.1.0/contrast-agent-5.1.0.jar
4	https://search.maven.org/remotecontent?filepath=com/contrastsecurity/contrast-agent/4.13.1/contrast-agent-4.13.1.jar
3	https://search.maven.org/remotecontent?filepath=com/contrastsecurity/contrast-agent/3.18.2/contrast-agent-3.18.2.jar
2	https://search.maven.org/remotecontent?filepath=com/contrastsecurity/contrast-agent/2.13.2/contrast-agent-2.13.2.jar
1	https://search.maven.org/remotecontent?filepath=com/contrastsecurity/contrast-agent/1.0/contrast-agent-1.0.jar
0	https://search.maven.org/remotecontent?filepath=com/contrastsecurity/contrast-agent/0.6/contrast-agent-0.6.jar
```

## Requirements

- Python 3.8 or newer

## Usage

1. `pip install -r requirements.txt`
1. `python redirect.py`

## Configuration

The following environment variables control behaviour:
- `REQUEST_TIMEOUT` - time in seconds that requests should timeout after. Default `5`.
- `REDIRECT_PREFIX` - string to prepend before `latest`/major version in the output. Default "" (empty string).