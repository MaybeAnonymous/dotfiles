#             _|      _|  _|
#   _|_|_|  _|_|_|_|      _|    _|_|
# _|    _|    _|      _|  _|  _|_|_|_|
# _|    _|    _|      _|  _|  _|
#   _|_|_|      _|_|  _|  _|    _|_|_|
#       _| tiling window managers are great
#       _| ( no wayland support, sorry )


import os
import subprocess
from typing import List  # noqa: F401

import psutil  # Used for window swallowing.

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
# from libqtile import hook

MOD = "mod4"

# > Commands
BROWSER = "librewolf"
ROFI_DRUN = "rofi -show drun -show-icons"
EMOJI = "rofi -show emoji"
FILE_MANAGER = "thunar"
FULL_SCREENSHOT = "sh -c 'maim | xclip -selection clipboard -t image/png'"
DMENU = "dmenu_run"
ROFI_RUN = "rofi -show run -show-icons"
SCREENSHOT = "sh -c 'maim -s -u | xclip -selection clipboard -t image/png'"
TERM = "kitty"

# > Control Commands
RAISE_VOL = "pamixer -i5"
LOWER_VOL = "pamixer -d5"
TOGGLE_MUTE = "pamixer -t"
RAISE_BR = "brightnessctl s 5%+"
LOWER_BR = "brightnessctl s 5%-"

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([home])


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html

    # > Window switching
    Key([MOD], "h", lazy.layout.left(),     desc = "Move focus to left"),
    Key([MOD], "l", lazy.layout.right(),    desc = "Move focus to right"),
    Key([MOD], "j", lazy.layout.down(),     desc = "Move focus down"),
    Key([MOD], "k", lazy.layout.up(),       desc = "Move focus up"),
    Key([MOD], "space", lazy.layout.next(), desc = "Move window focus to other window"),

    Key([MOD, "shift"], "h", lazy.layout.shuffle_left(),  desc = "Move window to the left"),
    Key([MOD, "shift"], "l", lazy.layout.shuffle_right(), desc = "Move window to the right"),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down(),  desc = "Move window down"),
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up(),    desc = "Move window up"),

    Key([MOD, "control"], "h", lazy.layout.grow_left(),  desc = "Grow window to the left"),
    Key([MOD, "control"], "l", lazy.layout.grow_right(), desc = "Grow window to the right"),
    Key([MOD, "control"], "j", lazy.layout.grow_down(),  desc = "Grow window down"),
    Key([MOD, "control"], "k", lazy.layout.grow_up(),    desc = "Grow window up"),
    Key([MOD], "n",            lazy.layout.normalize(),  desc = "Reset all window sizes"),

    Key(
        [MOD, "control"],
        "Return",
        lazy.layout.toggle_split(),
        desc = "Toggle between split and unsplit sides of stack",
    ),

    # > Menus
    Key([MOD], "p", lazy.spawn(DMENU), desc = "Launch dmenu"),
    Key([MOD, "shift"], "d", lazy.spawn(ROFI_DRUN)),
    Key([MOD, "control"], "d", lazy.spawn(ROFI_RUN)),
    Key([MOD], "period", lazy.spawn(EMOJI)),

    # > Layouts
    Key([MOD, "shift"], "e",     lazy.shutdown(),      desc = "Shutdown Qtile"),
    Key([MOD, "shift"], "f",     lazy.window.toggle_fullscreen()),
    Key([MOD, "shift"], "q",     lazy.window.kill(),   desc = "Kill focused window"),
    Key([MOD, "shift"], "r",     lazy.reload_config(), desc = "Reload the config"),
    Key([MOD, "shift"], "space", lazy.window.toggle_floating()),
    Key([MOD],          "r",     lazy.spawncmd(),      desc = "Spawn a command using a prompt widget"),
    Key([MOD],          "Tab",   lazy.next_layout(),   desc = "Toggle between layouts"),

    # > Screenshots
    Key([MOD, "shift"], "s", lazy.spawn(SCREENSHOT),      desc = "Take a selected screenshot"),
    Key([MOD, "shift"], "z", lazy.spawn(FULL_SCREENSHOT), desc = "Take a full screenshot"),

    # > Utilities
    Key([MOD,  "shift"], "Return", lazy.spawn(FILE_MANAGER), desc = "Launch file browser"),
    Key([MOD], "f",                lazy.spawn(BROWSER),      desc = "Launch the web browser"),
    Key([MOD], "Return",           lazy.spawn(TERM),         desc = "Launch terminal"),

    Key([],    "XF86AudioLowerVolume", lazy.spawn(LOWER_VOL)),
    Key([],    "XF86AudioMute",        lazy.spawn(TOGGLE_MUTE)),
    Key([],    "XF86AudioRaiseVolume", lazy.spawn(RAISE_VOL)),
    Key([],    "XF86MonBrightnessDown",lazy.spawn(LOWER_BR)),
    Key([],    "XF86MonBrightnessUp",  lazy.spawn(RAISE_BR))
]

# List from "1" to "9", the amount of desktops.
GROUPS = [Group(i) for i in "123456789"]

for i in GROUPS:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key([MOD], i.name, lazy.group[i.name].toscreen(),
                desc = "Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([MOD, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
                desc = "Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([MOD, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc = "move focused window to group {}".format(i.name)),
        ]
    )

MARGIN = 4
BORDER_WIDTH = 3
BORDER_FOCUS = "#a7c080"
BORDER_NORMAL = "#425047"

def init_basic_layout(margin, border_width, border_normal, border_focus):
    return {
            "margin": margin,  # Gap between windows.
            "border_width": border_width,
            "border_focus": border_focus,
            "border_normal": border_normal,
            "border_focus_stack": border_focus,
            "border_normal_stack": border_normal
    }
BASIC_LAYOUT = init_basic_layout(MARGIN, BORDER_WIDTH, BORDER_NORMAL, BORDER_FOCUS)

layouts = [
    layout.Columns(**BASIC_LAYOUT),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(**BASIC_LAYOUT),
    # layout.Stack(num_stacks=2),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    layout.Bsp(**BASIC_LAYOUT),
    # layout.Matrix(**BASIC_LAYOUT),
    layout.Max(**BASIC_LAYOUT),
    layout.Zoomy(**BASIC_LAYOUT),
]

widget_defaults = dict(
    font="Jetbrains Mono",
    fontsize=14,
    padding=5,
)
extension_defaults = widget_defaults.copy()

ACTIVE_TAG_FG = "#4f585e"
BG = "#232a2e"
FG = "#d3c6aa"
INACTIVE_TAG_FG = "#2d353b"
SELECTED = "#343f44"
SELECTED_FG = "#e69875"

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(foreground = FG),
                widget.GroupBox(active = ACTIVE_TAG_FG, inactive = INACTIVE_TAG_FG, highlight_method = "block",
                                block_highlight_text_color = SELECTED_FG, this_screen_border = SELECTED, 
                                this_current_screen_border = SELECTED, rounded = False,
                                padding = 4, disable_drag = True),
                widget.Prompt(foreground = FG),
                widget.WindowName(foreground = FG),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox("☀️", foreground = FG),
                widget.Backlight(foreground = FG, backlight_name = "intel_backlight"),
                widget.TextBox("| 📢", foreground = FG),
                widget.PulseVolume(foreground = FG, get_volume_command = "pamixer"),
                widget.TextBox("| 🔋", foreground = FG),
                widget.Battery(charge_char = "🔺", discharge_char = "🔻", empty_char = "🪫",
                               notify_below = 15, notification_timeout = 5,
                               update_interval = 2, foreground = FG),
                widget.TextBox("|", foreground = FG),
                widget.Clock(format="📅 %Y-%m-%d (%a) %H:%M", foreground = FG),
                widget.Systray(),
            ],
            28,  # Height of bar.
            background = BG,
            
            # Top, right, bottom and left.
            margin = [0, 0, MARGIN, 0]

            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        wallpaper = '~/.config/wallpaper.png',
        wallpaper_mode = 'fill',
    ),
]

# Drag floating layouts.
mouse = [
    Drag([MOD], "Button1", lazy.window.set_position_floating(), start = lazy.window.get_position()),
    Drag([MOD], "Button3", lazy.window.set_size_floating(), start = lazy.window.get_size()),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = False
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class = "confirmreset"),  # gitk
        Match(wm_class = "makebranch"),  # gitk
        Match(wm_class = "maketag"),  # gitk
        Match(wm_class = "ssh-askpass"),  # ssh-askpass
        Match(title = "branchdialog"),  # gitk
        Match(title = "pinentry"),  # GPG key password entry
    ],
    border_width = BORDER_WIDTH,
    border_focus = BORDER_FOCUS,
    border_normal = BORDER_NORMAL,
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# Be careful here! I got this from https://github.com/qtile/qtile/issues/1771.
# It does window swallowing, although I don't know how it works.
@hook.subscribe.client_new
def _swallow(window):
    pid = window.window.get_net_wm_pid()
    ppid = psutil.Process(pid).ppid()
    cpids = {c.window.get_net_wm_pid(): wid for wid, c in window.qtile.windows_map.items()}
    for i in range(5):
        if not ppid:
            return
        if ppid in cpids:
            parent = window.qtile.windows_map.get(cpids[ppid])
            if parent.window.get_wm_class()[0] != "Alacritty":
                return
            parent.minimized = True
            window.parent = parent
            return
        ppid = psutil.Process(ppid).ppid()

@hook.subscribe.client_killed
def _unswallow(window):
    if hasattr(window, 'parent'):
        window.parent.minimized = False

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
