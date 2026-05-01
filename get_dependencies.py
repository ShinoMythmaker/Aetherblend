import json
import os
import tomllib
import tomli_w
import urllib.request

MANIFEST_FILENAME = "blender_manifest.toml"
WHEELS_DIR = './wheels'
PYTHON_VERSIONS = ['cp311', 'cp313']

def download_package_wheels(package_name: str) -> list:
    filenames = []

    pypi_json_url = urllib.request.urlopen(f'https://pypi.org/pypi/{package_name}/json')
    pypi_json_data = pypi_json_url.read()
    pypi_json = json.loads(pypi_json_data.decode('utf-8'))

    releases = pypi_json['releases']
    latest_release = next(reversed(releases))

    for item in releases[latest_release]:
        if (item['yanked'] == True or
            item['packagetype'] != 'bdist_wheel' or
            item['python_version'] not in PYTHON_VERSIONS):
            continue

        filename = item['filename']
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
    
    del manifest['dependencies']

    with open(MANIFEST_FILENAME, 'wb') as f:
        tomli_w.dump(manifest, f)

if __name__ == '__main__':
    main()
