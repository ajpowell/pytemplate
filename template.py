import logging
import sys
import os
import json
import argparse
from dotenv import load_dotenv

'''
template.py

Python venv
===========
Full details here: https://docs.python.org/3/library/venv.html
Short version:
    python -m venv ./venv

Activate venv with:
    Mac/Linux   source ./venv/bin/activate
    Windows     .\\venv\\Scripts\\Activate.ps1

Update pip, if required:
    ./venv/bin/python -m pip install --upgrade pip

Requirements.txt
================
# Full details here: https://datagy.io/python-requirements-txt/
# Create requirements.txt by running:
pip3 freeze > requirements.txt

# Install required modules using:
pip3 install -r requirements.txt

# List any outdated modules
pip3 list --outdated

# Upgrade specific modules
pip3 install -U package_name

Create deployable wheel
=======================
# Full details here: https://pip.pypa.io/en/stable/cli/pip_wheel/

# Install setup tools
python -m pip install -U wheel setuptools

# Build wheel package
pip wheel . -w wheels

# Deploy a wheel file
pip install package-1.0-cp27-none-macosx_10_7_intel.whl

Arguments
=========
Simple approach - accepts:
    -v - reports version only
    -d - runs in debug mode for logging
    -q - runs in quiet mode
    -h - show help

Advanced arguments:
https://docs.python.org/3/library/argparse.html



Logging
=======
Defaults to INFO level - use -d to include DEBUG

Configuration
=============
Simple json file (config.json)

'''

#     Ver    Author          Date       Comments
#     ===    =============== ========== =======================================
ver = 0.1  # ajpowell        2022-06-14 Initial code
ver = 0.2  # ajpowell        2022-06-22 Minor corrections
ver = 0.3  # ajpowell        2023-02-27 More minor updates
ver = 0.4  # ajpowell        2023-03-02 Using argparse

config_filename = 'config.json'

parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description='Project description...',
        epilog='Epilog text...'
        )


def configure_logging():
    # Initialise logging module
    logging.root.handlers = []
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        # datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
        # level=logging.DEBUG
        )


def parse_args():
    parser.add_argument('-v', '--version',
                        action='store_true', help='Show version')
    parser.add_argument('-d', '--debug',
                        action='store_true', help='Debug mode')
    parser.add_argument('-q', '--quiet',
                        action='store_true', help='Quiet mode')

    return parser.parse_args()


def main():
    # Pulling the configuration from file
    config = None

    with open(config_filename, 'r') as f:
        config = json.load(f)

    if config is None:
        logging.error('ERROR: There was a problem loading the config file [{}]'.format(config_filename))  # noqa: E501
        sys.exit(-1)

    test_data = config['test']

    logging.info('Data (from config.json): {}'.format(test_data))

    logging.info('Starting...')

    # Read envs that came from .env
    env = os.environ.get("ENV")

    logging.info('Environment (from .env): {}'.format(env))

    # Read environment variables from OS
    try:
        env_shell = os.getenv('SHELL')
        logging.info('Shell: {}'.format(env_shell))

    except Exception as ex:
        # except Exception:
        # Handle the exception
        logging.error('An error ocurred getting the environment variable')
        logging.error(ex)

    else:
        logging.debug('Debug output...')
        logging.info('Nearly done...')
        logging.info('Done.')
        print('')
        sys.exit(1)

    logging.debug('Debug output...')
    logging.info('Nearly done...')

    # save config
    # config['last_number'] = last_number

    # write config back to the file
    with open(config_filename, 'w') as f:
        json.dump(config, f)

    logging.info('Done.')
    print('')


if __name__ == "__main__":
    configure_logging()

    # Load the environment variables from .env
    load_dotenv()

    logging.info('{} v{}'.format(os.path.basename(__file__), ver))

    # Simple argument handling
    # if len(sys.argv) > 1:
    #    # Just exit if -v supplied on command line
    #    if sys.argv[1].lower() == '-v':
    #    # If -d then enable debug mode
    #        sys.exit()
    #        logging.getLogger().setLevel(logging.DEBUG)
    #        logging.debug('****** Debug mode enabled ******')
    #    # If -q then enable quiet mode
    #    if sys.argv[1].lower() == '-d':
    #    if sys.argv[1].lower() == '-q':
    #        logging.getLogger().setLevel(logging.WARNING)

    # Advanced argument handling
    args = parse_args()
    if args.version:
        sys.exit()

    if args.debug & args.quiet:
        print('Invalid combination of options.')
        parser.print_help()
        sys.exit()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('****** Debug mode enabled ******')

    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)

    # Jump to main code
    main()
