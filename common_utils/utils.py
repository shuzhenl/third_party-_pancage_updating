import os
# import shutil
import subprocess
import logging
from config import config as Config
logger = logging.getLogger()


def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def remove_dir(dir):
    command = "rm -rf '%s'" % dir
    logger.info("going to run command %s", command)
    return subprocess.check_output(command,
                                   universal_newlines=True,
                                   shell=True,
                                   cwd=dir)


def generate_report_dir(instance_id):
    report_dir = os.path.join(
        Config.BASE_DIR,
        Config.REPORT_SAVE_RELATIVE_PATH,
        str(instance_id)
    )
    ensure_dir(report_dir)
    return report_dir

