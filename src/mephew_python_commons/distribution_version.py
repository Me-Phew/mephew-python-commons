"""Read a project's version from installed metadata or its pyproject.toml."""

import inspect
import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def distribution_version(distribution_name: str) -> str:
    """Return the version of ``distribution_name``.

    Installed distributions are read from package metadata, which the build
    copies from ``[project].version``. Virtual projects are not installed, so
    metadata is missing when tests import them from the source tree. In that
    case the version is read from the nearest ancestor ``pyproject.toml``
    whose project name matches.
    """
    try:
        return version(distribution_name)
    except PackageNotFoundError as exc:
        discovered = _version_from_caller_pyproject(distribution_name)
        if discovered is not None:
            return discovered
        raise RuntimeError(f"{distribution_name} is not installed; cannot read its version") from exc


def _version_from_caller_pyproject(distribution_name: str) -> str | None:
    frame = inspect.currentframe()
    frame = frame.f_back if frame is not None else None
    frame = frame.f_back if frame is not None else None
    seen: set[Path] = set()
    while frame is not None:
        filename = frame.f_code.co_filename
        if filename.startswith("<"):
            frame = frame.f_back
            continue
        start = Path(filename).resolve()
        if start not in seen:
            seen.add(start)
            discovered = _matching_pyproject_version(start, distribution_name)
            if discovered is not None:
                return discovered
        frame = frame.f_back
    return None


def _matching_pyproject_version(start: Path, distribution_name: str) -> str | None:
    directory = start.parent if start.is_file() else start
    for candidate in (directory, *directory.parents):
        pyproject_path = candidate / "pyproject.toml"
        if not pyproject_path.is_file():
            continue
        try:
            with pyproject_path.open("rb") as pyproject_file:
                data = tomllib.load(pyproject_file)
        except tomllib.TOMLDecodeError:
            continue
        project = data.get("project")
        if not isinstance(project, dict):
            continue
        project_name = project.get("name")
        project_version = project.get("version")
        if (
            isinstance(project_name, str)
            and isinstance(project_version, str)
            and _normalized_name(project_name) == _normalized_name(distribution_name)
        ):
            return project_version
    return None


def _normalized_name(name: str) -> str:
    return name.lower().replace("_", "-").replace(".", "-")
