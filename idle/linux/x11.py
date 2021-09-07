import ctypes
import ctypes.util

__all__ = ["idle"]

exception = None
"""If an exceptions occurs during setup, the module will be imported silently, but idle_xss() will raise it."""

class XScreenSaverInfo(ctypes.Structure):
    _fields_ = [
        ('window', ctypes.c_ulong),
        ('state', ctypes.c_int),
        ('kind', ctypes.c_int),
        ('til_or_since', ctypes.c_ulong),
        ('idle', ctypes.c_ulong),
        ('eventMask', ctypes.c_ulong)
    ]

XScreenSaverInfo_p = ctypes.POINTER(XScreenSaverInfo)

display_p = ctypes.c_void_p
xid = ctypes.c_ulong
c_int_p = ctypes.POINTER(ctypes.c_int)

libX11path = ctypes.util.find_library('X11')
if libX11path is None:
    exception = OSError('libX11 could not be found.')
libX11 = ctypes.cdll.LoadLibrary(libX11path)
libX11.XOpenDisplay.restype = display_p
libX11.XOpenDisplay.argtypes = (ctypes.c_char_p,)
libX11.XDefaultRootWindow.restype = xid
libX11.XDefaultRootWindow.argtypes = (display_p,)

libXsspath = ctypes.util.find_library('Xss')
if libXsspath is None:
    exception = OSError('libXss could not be found.')
libXss = ctypes.cdll.LoadLibrary(libXsspath)
libXss.XScreenSaverQueryExtension.argtypes = display_p, c_int_p, c_int_p
libXss.XScreenSaverAllocInfo.restype = XScreenSaverInfo_p
libXss.XScreenSaverQueryInfo.argtypes = (display_p, xid, XScreenSaverInfo_p)

dpy_p = libX11.XOpenDisplay(None)
if dpy_p is None:
    exception = OSError('Could not open X Display.')

_event_basep = ctypes.c_int()
_error_basep = ctypes.c_int()
extension = libXss.XScreenSaverQueryExtension(dpy_p, ctypes.byref(_event_basep), ctypes.byref(_error_basep))
if extension == 0:
    exception = OSError('XScreenSaver Extension not available on display.')

xss_info_p = libXss.XScreenSaverAllocInfo()
if xss_info_p is None:
    exception = OSError('XScreenSaverAllocInfo: Out of Memory.')

rootwindow = libX11.XDefaultRootWindow(dpy_p)

def idle():
    try:
        if exception is not None:
            raise exception

        e = libXss.XScreenSaverQueryInfo(dpy_p, rootwindow, xss_info_p)
        if e == 0:
            raise RuntimeError
        return xss_info_p.contents.idle / 1000
    except OSError as error:
        raise OSError("unable to query idle time for this system") from error
