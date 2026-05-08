import json
import os
import re
import tomllib
import tomli_w
import urllib.request

MANIFEST_FILENAME = "blender_manifest.toml"
WHEELS_DIR = './wheels'
PYTHON_VERSIONS = ['cp311', 'cp313']

# PEP 427 wheel filename parser (name-version-(-build)?-python-abi-platform.whl)
WHEEL_FILENAME_RE = re.compile(
    r'^(?P<name>.+?)-(?P<version>.+?)'
    r'(?:-(?P<build>\d[^-]*))?'
    r'-(?P<python_tag>[^-]+)-(?P<abi_tag>[^-]+)-(?P<platform_tag>[^-]+)\.whl$'
)


def is_supported_wheel(filename: str) -> bool:
    """Return True when wheel tags match our supported Python/ABI targets.
    """
    match = WHEEL_FILENAME_RE.match(filename)
    if match is None:
        return False

    python_tags = set(match.group('python_tag').split('.'))
    abi_tags = set(match.group('abi_tag').split('.'))

    has_supported_python_tag = (
        bool(python_tags.intersection(PYTHON_VERSIONS)) or
        any(tag.startswith('py3') for tag in python_tags)
    )
    if not has_supported_python_tag:
        return False

    # Exclude free-threaded ABI wheels such as cp313t.
    if any(tag.startswith('cp') and tag.endswith('t') for tag in abi_tags):
        return False

    return True

def download_package_wheels(package_name: str) -> list:
    filenames = []

    pypi_json_url = urllib.request.urlopen(f'https://pypi.org/pypi/{package_name}/json')
    pypi_json_data = pypi_json_url.read()
    pypi_json = json.loads(pypi_json_data.decode('utf-8'))

    releases = pypi_json['releases']
    latest_release = next(reversed(releases))

    for item in releases[latest_release]:
        if item['yanked'] == True or item['packagetype'] != 'bdist_wheel':
            continue

        filename = item['filename']
        if not is_supported_wheel(filename):
            continue

        path = f'{WHEELS_DIR}/{filename}'
        urllib.request.urlretrieve(item['url'], path)
        filenames.append(path)

    return filenames

def main():
    if not os.path.isfile(MANIFEST_FILENAME):
        print(f'[get_dependencies.py] Error: {MANIFEST_FILENAME} was not found.')
        exit(1)

    with open(MANIFEST_FILENAME, 'rb') as f:
        manifest = tomllib.load(f)

    manifest['wheels'] = []

    os.makedirs(WHEELS_DIR, exist_ok=True)

    for dependency in manifest['dependencies']:
        dependency_wheels = download_package_wheels(dependency)

        for wheel in dependency_wheels:
            manifest['wheels'].append(wheel)

    with open(MANIFEST_FILENAME, 'wb') as f:
        tomli_w.dump(manifest, f)

if __name__ == '__main__':
    main()
