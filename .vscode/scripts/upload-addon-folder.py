#!/usr/bin/env python

"""Upload addon zip using ayon-python-api.

It's used to upload addons versions that epcified as arguments.
It requires having a .env file with the following keys:
- 'AYON_SERVER_URL': AYON server URL
- 'AYON_API_KEY': AYON service user api key

Script usage examples:
  python upload-addon-folder.py --addon ayon-core --addon ayon-nuke
Support flags:
'--debug': used to make log more verbose.
'--addon' ('-a'): used to specify addon repo full path, it'll be used to get addon zip name.

Notes:
    users must at least one of these flags '--addon or '--package-dir'.
    if '--package-dir' not found, the code will fall to default package dir in the given addon paths.
    if '--addon' not found, the code will upload all packages found in the given package dir.

"""

import argparse
import logging
import os
import sys
from pathlib import Path

try:
    import ayon_api
    from ayon_api import get_server_api_connection

    has_ayon_api = True
except ModuleNotFoundError:
    has_ayon_api = False

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    if has_ayon_api:
        logging.warning("dotenv not installed, skipping loading .env file")

scripts_dir = Path(__file__).resolve().parent
workspace_dir = Path(__file__).resolve().parent.parent.parent

docker_addons_dir = workspace_dir / "ayon-docker" / "addons"

python_exe = sys.executable

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="Debug log messages."
    )
    parser.add_argument(
        "-a",
        "--addon",
        dest="addons",
        action="append",
        help="Addon repo name to upload.",
        required=True,
    )

    args = parser.parse_args(sys.argv[1:])

    # Set Log Level and create log object
    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(level=level)
    log: logging.Logger = logging.getLogger("upload_package")

    repo_folders = os.listdir(workspace_dir.as_posix())
    processed_addons = []
    for addon in args.addons:
        if addon not in repo_folders:
            continue
        addon_repo_dir = workspace_dir / addon
        args = (
            f"{python_exe} {addon_repo_dir.as_posix()}/create_package.py "
            f"--skip-zip --output {docker_addons_dir.as_posix()}"
        )
        log.info(f"Running: {args}")
        os.system(args)

        processed_addons.append(addon)

    if not processed_addons:
        log.error("No addons found to process.")
        sys.exit(1)

    # Log in and Try to upload addons
    ayon_api.init_service()
    log.info("Trying restart server")

    server = get_server_api_connection()
    if server:
        server.trigger_server_restart()
    else:
        log.warning("Could not restart server")
