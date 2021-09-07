import subprocess as sp
import re

__all__ = ["idle"]

def idle():
    ioreg = sp.run(["ioreg", "-r", "-d1", "-c", "IOHIDSystem"],
        stdout=sp.PIPE, text=True, check=True).stdout
    m = re.search(idle.re_ioreg, ioreg)
    if not m:
        raise OSError("could not find HIDIdleTime property in MacOS I/O Kit registry")
    return float(m.group(1)) / 10**9

idle.re_ioreg = re.compile(r"\"HIDIdleTime\" = (\d+)")
