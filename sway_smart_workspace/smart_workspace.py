import argparse
import re
import shutil
import time
from pathlib import Path

from i3ipc import Connection


def get_output():
    return """
output {name}

workspace {index}:1 output {name}
workspace {index}:2 output {name}
workspace {index}:3 output {name}
workspace {index}:4 output {name}
workspace {index}:5 output {name}
workspace {index}:6 output {name}
workspace {index}:7 output {name}
workspace {index}:8 output {name}
workspace {index}:9 output {name}
workspace {index}:10 output {name}
"""


def get_controls():
    return """
#  add the following line
#  include $HOME/.config/sway/outputs/*
#  into your main sway config to add the config below.
#  Remove those parts of the main sway config accordingly. 

bindsym $mod+1 exec "sway-smart-workspace -i 1"
bindsym $mod+2 exec "sway-smart-workspace -i 2"
bindsym $mod+3 exec "sway-smart-workspace -i 3"
bindsym $mod+4 exec "sway-smart-workspace -i 4"
bindsym $mod+5 exec "sway-smart-workspace -i 5"
bindsym $mod+6 exec "sway-smart-workspace -i 6"
bindsym $mod+7 exec "sway-smart-workspace -i 7"
bindsym $mod+8 exec "sway-smart-workspace -i 8"
bindsym $mod+9 exec "sway-smart-workspace -i 9"
bindsym $mod+0 exec "sway-smart-workspace -i 10"

bindsym $mod+Shift+1 exec "sway-smart-workspace -si 1"
bindsym $mod+Shift+2 exec "sway-smart-workspace -si 2"
bindsym $mod+Shift+3 exec "sway-smart-workspace -si 3"
bindsym $mod+Shift+4 exec "sway-smart-workspace -si 4"
bindsym $mod+Shift+5 exec "sway-smart-workspace -si 5"
bindsym $mod+Shift+6 exec "sway-smart-workspace -si 6"
bindsym $mod+Shift+7 exec "sway-smart-workspace -si 7"
bindsym $mod+Shift+8 exec "sway-smart-workspace -si 8"
bindsym $mod+Shift+9 exec "sway-smart-workspace -si 9"
bindsym $mod+Shift+0 exec "sway-smart-workspace -si 10"

bindsym $mod+Control+1 exec "sway-smart-workspace -ski 1"
bindsym $mod+Control+2 exec "sway-smart-workspace -ski 2"
bindsym $mod+Control+3 exec "sway-smart-workspace -ski 3"
bindsym $mod+Control+4 exec "sway-smart-workspace -ski 4"
bindsym $mod+Control+5 exec "sway-smart-workspace -ski 5"
bindsym $mod+Control+6 exec "sway-smart-workspace -ski 6"
bindsym $mod+Control+7 exec "sway-smart-workspace -ski 7"
bindsym $mod+Control+8 exec "sway-smart-workspace -ski 8"
bindsym $mod+Control+9 exec "sway-smart-workspace -ski 9"
bindsym $mod+Control+0 exec "sway-smart-workspace -ski 10"
"""


class WorkSpacer:
    def __init__(self, args):
        self.workspaces = None
        self.args = args
        self.outputs = None

        try:
            self.sway = Connection()
            self.outputs = self.sway.get_outputs()
        except Exception as e:
            pass
        if 'only_send' in args:
            self._send_msg(args.only_send)

    def _send_msg(self, msg):
        self.sway.command(f'exec "notify-send \'{msg}\'"')

    def _create_default_config(self, path: Path, name):
        # Count number of configs
        num = sum(1 for _ in Path(self.args.output_location).glob('*')) - 1  # don't include controls.py
        path.write_text(get_output().replace('{name}', name).replace('{index}', str(num)))

    def run(self):
        name = self._get_workspace_from_courser_position()
        output_config = Path(self.args.output_location).joinpath(name)
        if not output_config.exists():
            self._create_default_config(output_config, name)
        workspaces = []

        for matchNum, match in enumerate(
                re.finditer(r'workspace (.*) output (.*)', output_config.read_text(), re.MULTILINE)
        ):
            workspaces.append(match.group(1))

        if self.args.shift:
            self.sway.command(
                f'move container to workspace {workspaces[self.args.index - 1]}'
            )
            if not self.args.keep_with_it:
                return
        self.sway.command(f'workspace {workspaces[self.args.index - 1]}')

    def print_output_continuously(self):
        while True:
            print(self._get_workspace_from_courser_position())
            time.sleep(1)

    def _get_workspace_from_courser_position(self, full=False):
        for output in self.sway.get_outputs():
            if output.focused:
                res = f'{output.name}'
                if full:
                    res += f' {output.make} {output.model} {output.serial}'
                return res


default_home = Path.home().joinpath('.config').joinpath('sway').joinpath('outputs')


parser = argparse.ArgumentParser(
    description="Changes the workspace, based on what output your cursor is on."
)
parser.add_argument('-d', '--debug', action='store_true',
                    help='Turn on debug mode.')

required_group = parser.add_argument_group('Required', '')
required_group.add_argument("-i", "--index", type=int, required=True,
                            help="The indexed workspace for the output where the cursor is currently located")
required_group.add_argument('-o', '--output-location',
                            default=default_home,
                            help='The dir for where the location output configurations are located')

shift_group = parser.add_argument_group('Shift', 'manipulate the active window')
shift_group.add_argument("-s", "--shift", action='store_true',
                         help="Moves the active window to the index workspace")
shift_group.add_argument('-k', '--keep-with-it', action='store_true',
                         help='Moves the active window to the index workspace, and moves with it')


def main():
    parsed_args = parser.parse_args()
    if default_home == parsed_args.output_location:
        if not default_home.is_dir():
            default_home.mkdir(parents=True, exist_ok=True)
            default_home.joinpath('controls').write_text(get_controls())

            parsed_args['only_send'] = 'Before using this tool remember to add include $HOME/.config/sway/outputs to ' \
                                       'your configuration '
            WorkSpacer(parsed_args)
            exit()
    elif not Path(parsed_args.output_location).is_dir():
        raise Exception('--output-location MUST be a directory.')
    if parsed_args.debug:
        WorkSpacer(parsed_args).print_output_continuously()
    else:
        WorkSpacer(parsed_args).run()


if __name__ == '__main__':
    main()
