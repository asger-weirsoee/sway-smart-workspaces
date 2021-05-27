import re
import subprocess
import time
from pathlib import Path
from uinput import Device
from pymouse import PyMouse
import pynput
from i3ipc import Connection
from i3ipc import OutputReply


def get_active_outputs():
    ps = subprocess.Popen(('xrandr', '--listmonitors'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('awk', "{print $4}"), stdin=ps.stdout)
    ps.wait()
    return [x for x in output.decode('UTF-8').split('\n') if x is not None and x != '']


names_for_outputs = r'(' + '|'.join(get_active_outputs()) + ')'


class WorkSpacer:

    def __init__(self, args, template_position):
        self.workspaces = None
        self.args = args
        self.outputs = None
        self.template_position = template_position
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
        num = sum(1 for _ in Path(self.args.output_location).glob('*')) - 1  # don't include controls
        path.write_text(
            self.template_position.joinpath('output').read_text()
                .replace('{name}', name).replace('{index}', str(num)))

    def run(self):
        name = self._get_workspace_from_courser_position()
        print(name)
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

    def _get_workspace_from_courser_position(self):
        for output in self.sway.get_outputs():
            if output.focused:
                return output.name

