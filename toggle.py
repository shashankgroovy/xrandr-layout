#!/usr/bin/env python3
import gi
import os
import yaml

from toast import show_toast

# Specify the Gdk version before importing it.
gi.require_version("Gdk", "3.0")

from gi.repository import Gdk


# Laptop screen is the primary display and is named 'eDP1'
PRIMARY_SCREEN_NAME = "eDP1"

# Method to fetch monitor details via Gdk.
# With the advent of Gdk its best to use it to work with monitors or graphical
# interfaces over xrandr in Linux environments.
# For more read: https://lazka.github.io/pgi-docs/Gdk-3.0/classes/Monitor.html


def get_monitors():
    """ Returns a list of connected monitors """
    allmonitors = []

    gdkdsp = Gdk.Display.get_default()
    for i in range(gdkdsp.get_n_monitors()):
        monitor = gdkdsp.get_monitor(i)
        scale = monitor.get_scale_factor()
        geo = monitor.get_geometry()
        allmonitors.append(
            {
                "screen": monitor.get_model(),
                "height": scale * geo.height,
                "width": scale * geo.width,
            }
        )

    return allmonitors


def get_connected_monitors():
    """This method calls xrandr to return a list of connected monitors"""
    out = os.popen("xrandr").readlines()
    connected = list(
        map(lambda x: x.split(" ")[0], filter(lambda s: " connected " in s, out))
    )
    return connected


# Methods to interact with layout configuration file
# The CONFIG_FILES list contains the default naming convention expected for a
# layout config file


class Config:
    """Config defines layout configurations"""

    CONFIG_FILES = ["layout.yaml", "layout.yml"]

    def __init__(self):
        pass

    def config_exists(self):
        """Returns the name of layout configuration file if present else None"""

        for file in self.CONFIG_FILES:
            found = os.path.exists(file)
            if found:
                return file

        return None

    def get_config_layout(self, file):
        """Returns the current layout from the yaml file.

        Expected values are: primary, secondary or extended.
        """
        try:
            with open(file) as f:
                docs = yaml.full_load(f)
                layout = docs.get("layout", None)

                if layout is None:
                    # Bad config file
                    return None

                return layout

        except FileNotFoundError:
            # Yaml configuration is not present
            return None

    def save_config(self, file, conf):
        """Writes the current display setting to layout.yaml file"""
        try:
            with open(file, "w") as f:
                yaml.dump(conf, f)

        except FileNotFoundError:
            # Yaml configuration is not present
            pass


# Below we find methods that toggle the screens, and based on the
# configurations sets a layout.


def toggle():
    """Toggle checks monitor configurations and sets the desired monitor
    setting"""

    active_monitors = get_monitors()
    connected_monitors = get_connected_monitors()
    # cfile = config_exists()
    # conf = get_config_layout(cfile)

    if len(connected_monitors) > 1 and len(active_monitors) == 1:
        secondary = list(filter(lambda m: m != PRIMARY_SCREEN_NAME, connected_monitors))[0]
        if active_monitors[0]["screen"] == PRIMARY_SCREEN_NAME:
            toggle_secondary(secondary)
            turn_off(PRIMARY_SCREEN_NAME)
            show_toast("Monitor")

        elif active_monitors[0]["screen"] != PRIMARY_SCREEN_NAME:
            toggle_primary()
            turn_off(secondary)
            show_toast("Laptop")
    else:
        toggle_primary_resolution(active_monitors[0])

    # save_config(cfile, conf)
    refresh_i3()


def toggle_primary_resolution(monitor):
    """Change the resolution of primary display"""

    if monitor["width"] != 1920 and monitor["height"] != 1200:
        set_resolution(PRIMARY_SCREEN_NAME, 1920, 1200)
    else:
        set_resolution(PRIMARY_SCREEN_NAME, 2560, 1600)


def toggle_primary():
    """Switch to primary display"""
    set_resolution(PRIMARY_SCREEN_NAME, 1920, 1200)


def toggle_secondary(screen):
    """Switch to primary display"""
    set_resolution(screen, 2560, 1440)


# Below we define the methods that call external unix utilities like xrandr and
# i3 to do the needful.


def set_resolution(screen, width, height):
    """Calls xrandr to set given resolution on a screen"""
    os.system(f"xrandr --output {screen} --primary --mode {width}x{height}")


def turn_off(screen):
    """Calls xrandr to turn off a given screen"""
    os.system(f"xrandr --output {screen} --off")


def refresh_i3():
    """Reload i3's config"""
    os.system("i3-msg restart")


if __name__ == "__main__":
    toggle()
