import argparse
import shutil
from pathlib import Path

from . import WorkSpacer

template_position = Path(__file__).parent.joinpath('templates')

parser = argparse.ArgumentParser(
    description="Changes the workspace, based on what output your cursor is on."
)
parser.add_argument('-d', '--debug', action='store_true',
                    help='Turn on debug mode.')
default_home = Path().home().joinpath('.config').joinpath('sway').joinpath('outputs')

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
parsed_args = parser.parse_args()


def main():
    if default_home == parsed_args.output_location:
        if not default_home.is_dir():
            default_home.mkdir(parents=True, exist_ok=True)
            shutil.copy(template_position.joinpath('controls'), default_home.joinpath('controls'))
            parsed_args[
                'only_send'] = 'Before using this tool remember to add include $HOME/.config/sway/outputs to your configuration'
            WorkSpacer(parsed_args, template_position)
            exit()
    elif not Path(parsed_args.output_location).is_dir():
        raise Exception('--output-location MUST be a directory.')
    if parsed_args.debug:
        WorkSpacer(parsed_args, template_position).print_output_continuously()
    else:
        WorkSpacer(parsed_args, template_position).run()


if __name__ == '__main__':
    main()
