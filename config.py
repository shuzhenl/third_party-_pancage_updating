from pathlib import Path
import os

HOME_DIR = str(Path.home())
# BASE_DIR = os.path.join(HOME_DIR, "AAProj")


class Config(object):

    # base temp file dir
    BASE_DIR = os.path.join(HOME_DIR, "Code")

    # File save path
    GIT_REPO_RELATIVE_PATH = "repo"
    BUILD_SAVE_RELATIVE_PATH = "build"
    REPORT_SAVE_RELATIVE_PATH = "report"

    # log
    LOG_CONFIG_PATH = "logging.conf"

    # server address
    SERVER_ADDRESS = "gs_automation.citrte.net"

    # max process number to run test suite
    MAX_PROCESS = 2

    # for simctl
    DEFAULT_RUNTIME = 'iOS 11.3'

    # global config
    AGENT_TYPE = 'Mobile'  # iOS/Android/Mobile


__all__ = ["config"]
