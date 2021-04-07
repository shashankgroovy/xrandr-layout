# xrandr layout

![python shield](https://img.shields.io/github/pipenv/locked/python-version/shashankgroovy/xrandr-layout?color=%231DB954&style=flat-square)

A simple utility script that works with
[xrandr](https://wiki.archlinux.org/index.php/xrandr) to change/switch
between different layouts.

For now it works with my Arch installation with one external monitor setup
with i3wm and uses PyQt5 to show a little toast notification on the screen.

## Requirements
1. xrandr
2. Python 3.x
3. PyQt5

## Run

To install the necessary requirements simply run:
```
λ pipenv install
```

To start the app simply run:
```
λ python toggle.py
``` 

## Future updates

- [x] Show toast notification when display changes using PyQt.
- [ ] Finish the feature to save current screen layout configuration to a config yaml file
- [ ] Make it an installable package, so that it's just a pip install away :)

## License
[MIT License](http://mit-license.org/)

Copyright © 2021 Shashank Srivastav