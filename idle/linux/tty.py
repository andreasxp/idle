from datetime import datetime
import subprocess as sp

__all__ = ["idle"]

def idle():
    out = sp.run("stat $(tty) --format='%X'",
        shell=True, stdout=sp.PIPE, text=True, check=True
    ).stdout

    idle_from = datetime.fromtimestamp(int(out))
    now = datetime.now()
    return (now - idle_from).total_seconds()
