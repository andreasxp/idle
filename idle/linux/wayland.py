from gi.repository import Gio, GLib

__all__ = ["idle", "idle_freedesktop", "idle_gnome"]

# idle_freedesktop ===============================================================================================
def idle_freedesktop():
    (idle_time,) = idle_freedesktop.proxy.call_sync(
        'GetSessionIdleTime', None, Gio.DBusCallFlags.NO_AUTO_START, -1, None
    )
    return idle_time / 1000

idle_freedesktop.proxy = Gio.DBusProxy.new_for_bus_sync(
    Gio.BusType.SESSION,
    Gio.DBusProxyFlags.NONE,
    None,
    'org.freedesktop.ScreenSaver',
    '/org/freedesktop/ScreenSaver',
    'org.freedesktop.ScreenSaver',
    None
)

try:
    idle_freedesktop()
    idle_freedesktop.available = True
except GLib.Error:
    idle_freedesktop.available = False


# idle_gnome =====================================================================================================
def idle_gnome():
    (idle_time,) = idle_gnome.proxy.call_sync('GetIdletime', None, Gio.DBusCallFlags.NO_AUTO_START, -1, None)
    return idle_time / 1000

idle_gnome.proxy = Gio.DBusProxy.new_for_bus_sync(
    Gio.BusType.SESSION,
    Gio.DBusProxyFlags.NONE,
    None,
    'org.gnome.Mutter.IdleMonitor',
    '/org/gnome/Mutter/IdleMonitor/Core',
    'org.gnome.Mutter.IdleMonitor',
    None
)

try:
    idle_gnome()
    idle_gnome.available = True
except GLib.Error:
    idle_gnome.available = False


def idle():
    try:
        return idle_freedesktop()
    except GLib.Error:
        # Idle time via D-Bus not available
        pass

    try:
        return idle_gnome()
    except GLib.Error:
        # Idle time via D-Bus (GNOME) not available
        pass

    raise OSError("unable to query idle time for this system")
