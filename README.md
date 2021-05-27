About
=====

Simple program that allows sway to include configurations for several outputs allowing the user to have 10 workspaces for each output that they'll ever connect to. And by a combination of the usual controls and the cursor location change workspace only on the output that the focus is on.

This also allows for a more seameless interaction with how workspaces are openend.

Usage
=====

    usage: pi3-sway-workspace [-h] [-d] -i INDEX [-o OUTPUT_LOCATION] [-s] [-k]

    Changes the workspace, based on what output your cursor is on.

    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           Turn on debug mode.

    Required:

      -i INDEX, --index INDEX
                            The indexed workspace for the output where the cursor is currently located
      -o OUTPUT_LOCATION, --output-location OUTPUT_LOCATION
                            The dir for where the location output configurations are located

    Shift:
      manipulate the active window

      -s, --shift           Moves the active window to the index workspace
      -k, --keep-with-it    Moves the active window to the index workspace, and moves with it

Installation
============

Install using pip (recommended):

    pip install pi3-sway-workspace

Before using this script for what is meant to do, you need to call it once.

this creates a folder with the controls and outputs for the output that you currently are on

default location :: is \$HOME/.config/sway/outputs

if you wish to change which folder is used, the script needs to be called with the --output-location parameter else just call it like so:

    pi3-sway-workspace -i 1

Now that the controls and output configuration is created, you have to locate the place in you own sway config that usually handels these controls, and remove them. Instead, replace it with an include statement for where your outputs folder is located.

So in otherwords instead of:

    bindsym $mod+1 workspace number 1
    bindsym $mod+2 workspace number 2
    bindsym $mod+3 workspace number 3
    bindsym $mod+4 workspace number 4
    bindsym $mod+5 workspace number 5
    bindsym $mod+6 workspace number 6
    bindsym $mod+7 workspace number 7
    bindsym $mod+8 workspace number 8
    bindsym $mod+9 workspace number 9
    bindsym $mod+0 workspace number 10

    bindsym $mod+Shift+1 move container to workspace 1
    bindsym $mod+Shift+2 move container to workspace 2
    bindsym $mod+Shift+3 move container to workspace 3
    bindsym $mod+Shift+4 move container to workspace 4
    bindsym $mod+Shift+5 move container to workspace 5
    bindsym $mod+Shift+6 move container to workspace 6
    bindsym $mod+Shift+7 move container to workspace 7
    bindsym $mod+Shift+8 move container to workspace 8
    bindsym $mod+Shift+9 move container to workspace 9
    bindsym $mod+Shift+0 move container to workspace 10

You should have

    include $HOME/agw/.config/sway/output/*

Now reload you sway configuration and you are good to go.

Future work
===========

Here a few ideas on how to improve pi3-smart-workspace could be improved in the future. If anyone wants to submit a pr that solves one of the problems stated below feel free to do so :)

-   Automatically yeet the default sway configuration of the worksapaces so that a more smooth install can happen
-   Never install something with pip in the global sence is kinda a bummer here, so an aur package would probably be good.

Credits
=======

Thanks to Michał Wieluński for an inspiration ([pi3-switch](https://github.com/landmaj/pi3-switch)) and Tony Crisci for an easy-to-use i3 python library ([i3ipc-python](https://github.com/acrisci/i3ipc-python)).
