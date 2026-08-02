"""core package initializer

This package exposes common core utilities and acts as a single Python
package root for the application. Subdirectories under `core/` are intended
to be plain directories containing modules and resources; they should not
require their own __init__.py files unless you explicitly want them to be
regular Python packages.

Example usage:
    from core import config
    from core import application

Keep this file minimal to avoid importing heavy modules at package import time.
"""

__version__ = "0.1"

# convenience imports (lazy import recommended in modules)
__all__ = ["config", "application", "runtime", "messaging", "assets", "api"]
