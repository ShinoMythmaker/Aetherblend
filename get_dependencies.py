"""Download the add-on's Python dependencies into the wheels folder."""

import json
import os
import re
import sys
import time
import tomllib
import urllib.error
import urllib.request

import tomli_w

MANIFEST_FILENAME = "blender_manifest.toml"
WHEELS_DIR = "./wheels"
PYTHON_VERSIONS = ["cp313"]

# PEP 427 wheel filename parser (name-version-(-build)?-python-abi-platform.whl)
WHEEL_FILENAME_RE = re.compile(
    r"^(?P<name>.+?)-(?P<version>.+?)"
    r"(?:-(?P<build>\d[^-]*))?"
    r"-(?P<python_tag>[^-]+)-(?P<abi_tag>[^-]+)-(?P<platform_tag>[^-]+)\.whl$"
)


def is_free_threaded_wheel(filename: str) -> bool:
    """Return whether a wheel targets a free-threaded CPython ABI."""
    match = WHEEL_FILENAME_RE.match(filename)
    if match is None:
        return False
    return any(tag.startswith("cp") and tag.endswith("t") for tag in match.group("abi_tag").split("."))


def print_status(message: str, color: str = "36", *, error: bool = False) -> None:
    """Print a status message with color when the output supports it."""
    stream = sys.stderr if error else sys.stdout
    use_color = (stream.isatty() or os.environ.get("GITHUB_ACTIONS") == "true") and "NO_COLOR" not in os.environ
    text = f"[get_dependencies.py] {message}"
    print(f"\033[{color}m{text}\033[0m" if use_color else text, file=stream)


def remove_obsolete_wheels() -> int:
    """Remove Python 3.11 and free-threaded wheel files from the wheels directory."""
    removed = 0
    with os.scandir(WHEELS_DIR) as entries:
        for entry in entries:
            match = WHEEL_FILENAME_RE.match(entry.name)
            if match is None or not entry.is_file(follow_symlinks=False):
                continue
            python_tags = match.group("python_tag").split(".")
            python_311_only = python_tags == ["cp311"] and match.group("abi_tag") != "abi3"
            if python_311_only or is_free_threaded_wheel(entry.name):
                os.remove(entry.path)
                removed += 1
                print_status(f"Removed obsolete wheel: {entry.name}", "33")
    return removed


def is_supported_wheel(filename: str) -> bool:
    """Return True when wheel tags match our supported Python/ABI targets."""
    match = WHEEL_FILENAME_RE.match(filename)
    if match is None:
        return False

    python_tags = set(match.group("python_tag").split("."))

    has_supported_python_tag = bool(python_tags.intersection(PYTHON_VERSIONS)) or any(tag.startswith("py3") for tag in python_tags)
    if not has_supported_python_tag:
        return False

    # Exclude free-threaded ABI wheels such as cp313t.
    if is_free_threaded_wheel(filename):
        return False

    return True


def download_package_wheels(package_name: str) -> list[str]:
    """Download supported wheels for a package."""
    filenames = []

    with urllib.request.urlopen(f"https://pypi.org/pypi/{package_name}/json") as response:
        pypi_json_data = response.read()
    pypi_json = json.loads(pypi_json_data.decode("utf-8"))

    releases = pypi_json["releases"]
    latest_release = next(reversed(releases))

    for item in releases[latest_release]:
        if item["yanked"] or item["packagetype"] != "bdist_wheel":
            continue

        filename = item["filename"]
        if not is_supported_wheel(filename):
            continue

        path = f"{WHEELS_DIR}/{filename}"
        urllib.request.urlretrieve(item["url"], path)
        filenames.append(path)
        print_status(f"Downloaded: {filename}")

    if not filenames:
        raise ValueError(f"No supported wheels were found for {package_name} ({latest_release}).")
    return filenames


def main() -> int:
    """Download required wheels, print a recap, and return an exit code."""
    started = time.monotonic()
    removed = 0
    completed_packages = 0
    downloaded_wheels: list[str] = []
    stage = f"reading {MANIFEST_FILENAME}"
    print_status("Preparing dependency wheels...")
    try:
        with open(MANIFEST_FILENAME, "rb") as file:
            manifest = tomllib.load(file)

        manifest["wheels"] = []

        stage = "removing obsolete wheels"
        os.makedirs(WHEELS_DIR, exist_ok=True)
        removed = remove_obsolete_wheels()

        for dependency in manifest["dependencies"]:
            stage = f"downloading {dependency}"
            print_status(f"Downloading supported wheels for {dependency}...")
            dependency_wheels = download_package_wheels(dependency)
            downloaded_wheels.extend(dependency_wheels)
            completed_packages += 1

        manifest["wheels"] = downloaded_wheels
        downloaded_size = sum(os.path.getsize(path) for path in downloaded_wheels)
        stage = f"writing {MANIFEST_FILENAME}"
        with open(MANIFEST_FILENAME, "wb") as file:
            tomli_w.dump(manifest, file)

    except (OSError, urllib.error.URLError, ValueError, KeyError, TypeError) as exc:
        print_status(f"FAILED while {stage}: {exc}", "31", error=True)
        print_status(
            f"Recap: {completed_packages} packages completed; {len(downloaded_wheels)} wheels from completed packages. "
            "Partial downloads or cleanup may remain on disk.",
            "31",
            error=True,
        )
        return 1

    print_status("SUCCESS: Dependency wheels downloaded and manifest updated.", "32")
    print_status(
        f"Recap: {completed_packages} packages; {len(downloaded_wheels)} wheels ({downloaded_size / 1024**2:.2f} MiB); "
        f"{removed} obsolete wheels removed; {time.monotonic() - started:.1f}s elapsed.",
        "32",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
