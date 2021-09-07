"""Linux-based idle checking code.

Some code is adapted from https://dev.gajim.org/gajim/gajim/-/blob/master/gajim/common/idle.py
"""
import subprocess as sp

__all__ = ["idle", "windowsystem"]

# Determine window manager
windowsystem = sp.run("loginctl show-session $(loginctl | grep $(whoami) | awk 'NR==1{print $1}') -p Type",
    shell=True, stdout=sp.PIPE, text=True, check=True
).stdout[5:-1]
# stout is something like: Type=wayland\n

if windowsystem == "x11":
    from .x11 import idle
elif windowsystem == "wayland":
    from .wayland import idle
elif windowsystem == "tty":
    from .tty import idle
else:
    def idle():
        raise OSError("unable to query idle time for this system")
