#!/usr/bin/env python
#
# 1. Discover any missing versions of the library.
# 2. Try to build a docker image with every missing version.
# 3. If the image we built passes the tests, create a new git tag.
#    Otherwise, fail the pipeline so we get notified.
#

import sys
import json
import subprocess
from urllib import request    
from pkg_resources import parse_version


PACKAGE_NAME = 'mlflow'

def run_or_fail(command: list):
    completed_process = subprocess.run(command, capture_output=True)
    if completed_process.returncode != 0:
        sys.exit(completed_process)

    return completed_process.stdout.decode('utf-8').strip()
        
def package_versions(package_name: str):
    url = f"https://pypi.python.org/pypi/{package_name}/json"
    return json.loads(request.urlopen(url).read())['releases']

def git_tags():
    return run_or_fail(['git', 'tag']).split("\n")

def sort(versions: list):
    return sorted(versions, key=parse_version)    

def build_docker_image(package_name: str, version: str):
    image_name = f"{package_name}:{version}"
    output = run_or_fail([
        'docker', 'build',
        '--build-arg', f"version={version}",
        '-t', image_name,
        '.'
    ])
    return image_name, output

versions_in_pypi = sort(package_versions(PACKAGE_NAME))
print(f"Versions of {PACKAGE_NAME} in PyPi:", versions_in_pypi)

versions_in_git = sort(git_tags())
print(f"Git tags:", versions_in_git)

missing_versions = {v for v in versions_in_pypi if parse_version(v) >= parse_version('1.0.0')} - set(versions_in_git)
print(f"Missing versions:", sort(list(missing_versions)))

for version in missing_versions:
    print(f"Building image for version {version}...")
    image_name, build_output = build_docker_image(PACKAGE_NAME, version)
    print(f"Built docker image {image_name}:\n{build_output}")

    version_output = run_or_fail(['docker', 'run', '--entrypoint=mlflow', image_name, '--version'])
    print(f"`mlflow --version` returned {version_output}")

    help_output = run_or_fail(['docker', 'run', image_name, '--help'])
    print(f"`mlflow server --help` returned {help_output}")

    print("Adding a git tag with version {version}")
    run_or_fail(['git', 'tag', version])


print('Pushing all tags...')
# run_or_fail(['git', 'push', 'origin', '--tags'])

