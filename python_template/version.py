import importlib.metadata
import re
from pathlib import Path

from loguru import logger


def get_version() -> str:
    # Try to read from pyproject.toml if running from source
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    if pyproject_path.exists():
        # regex for version=...
        content = pyproject_path.read_text()
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            logger.info("Version read from pyproject.toml: {}", match.group(1))
            return match.group(1)

    # Fallback to installed package metadata
    try:
        installed_version = importlib.metadata.version(__package__ or __name__)
        logger.info("Version read from package metadata: {}", installed_version)
        return installed_version
    except importlib.metadata.PackageNotFoundError:
        logger.warning("Package not found for version retrieval.")
        return "unknown"


__version__: str = get_version()
