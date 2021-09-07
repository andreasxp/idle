import sys

__all__ = ["idle"]

if sys.platform == "win32":
    from .windows import idle
elif sys.platform == "darwin":
    from .macos import idle
else:
    from .linux import idle
