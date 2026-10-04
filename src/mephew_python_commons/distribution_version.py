"""Read the version of an installed Python distribution."""

from importlib.metadata import PackageNotFoundError, version


def distribution_version(distribution_name: str) -> str:
    """Return the installed version of ``distribution_name``.

    The value comes from package metadata, which the build copies from
    ``[project].version`` in ``pyproject.toml``.
    """
    try:
        return version(distribution_name)
    except PackageNotFoundError as exc:
        raise RuntimeError(f"{distribution_name} is not installed; cannot read its version") from exc
