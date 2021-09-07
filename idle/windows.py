import win32api

__all__ = ["idle"]

def idle():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000
