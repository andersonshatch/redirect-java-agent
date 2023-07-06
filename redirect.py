from json import dumps as json_dumps, load as json_load, JSONDecodeError
from pathlib import Path
from typing import List
from urllib.parse import urlparse
import re
import os


VERSION_PATTERN = re.compile("\d+(\.)+")


def route_redirect(version: str, dest: str, status_code: int = 302):
    """Return a route redirect structure for the given version and destination"""
    return {"route": version, "redirect": dest, "statusCode": status_code}


def extract_version_from_url(url: str) -> str | None:
    """Extract version from a provided URL, the version is expected to be the first path segment matching the version pattern"""
    url_parts = urlparse(url)
    path = url_parts.path
    segments = path.split("/")
    version = next(
        (segment for segment in segments if VERSION_PATTERN.match(segment)), None
    )

    return version


def extract_major_version(version: str) -> int:
    """Extract the major version from a version string, i.e. leftmost digit(s) before the period"""
    return int(version.split(".")[0])


# Check input is provided or exit
new_version_url = os.environ.get("NEW_VERSION_URL")
if not new_version_url:
    print("ERROR: No NEW_VERSION_URL environment variable given, exiting")
    exit(1)
print(f"NEW_VERSION_URL: {new_version_url}")

# Check we can find the version from input or exit
new_version = extract_version_from_url(new_version_url)
if not new_version:
    print("ERROR: Unable to extract version from provided URL, exiting")
    exit(1)

# Inputs were validated successfully
print(f"Extracted version: {new_version}")
major_version = extract_major_version(new_version)
print(f"Major version: {major_version}")

# Load config file
output_dir = Path("publish")
output_file = output_dir / Path("staticwebapp.config.json")
try:
    config = json_load(output_file.open())
except JSONDecodeError as e:
    print(f"ERROR: could not load {output_file}", e)
    exit(1)
routes: List[dict] = config["routes"]

# Find "latest" route
latest_route: dict = next(filter(lambda route: route["route"] == "latest", routes))

# Find latest major routes and keep them in a dict (major_version -> route redirect structure)
major_routes: List[int:dict] = dict(
    ((int(route["route"]), route) for route in routes if route["route"].isdigit())
)

# Find any other routes
other_routes: List[dict] = filter(
    lambda route: route["route"] != "latest" and not route["route"].isdigit(), routes
)

latest_major_version = sorted(major_routes, reverse=True)[0]

# Version is a new major version if it is not already present in the routes list
new_major_version = major_version not in major_routes
# We should update the latest redirect if it is a new major version or an update to the existing major version
should_update_latest = new_major_version or major_version == latest_major_version
print(f"New major version: {new_major_version}")
print(f"Should update latest: {should_update_latest}")

redirect = route_redirect(str(major_version), new_version_url)
major_routes[major_version] = redirect
if should_update_latest:
    latest_route = route_redirect("latest", new_version_url)

# Preserve descending order of major routes
sorted_major_routes = list(
    (major_routes[route] for route in sorted(major_routes.keys(), reverse=True))
)

# Emit routes so "latest" is first, then all major versions in descending order, then any other routes
new_routes = [latest_route]
new_routes.extend(sorted_major_routes)
new_routes.extend(other_routes)

# Only override routes, keeping any other config
config["routes"] = new_routes

# Write new routes to file
output_file.write_text(json_dumps(config, indent=2))

# Print file contents to stdout
print("file contents:")
print(output_file.read_text())
