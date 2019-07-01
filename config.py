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


class ProdConfig(Config):
    IS_DEV = False
    SERVER_ADDRESS = "gs-autoauto-beta.citrite.net"


class DevConfig(Config):
    SERVER_ADDRESS = "127.0.0.1:8081"
    # GIT_REPO_RELATIVE_PATH = '/Users/yangwa/Automation/secure-web-automation'
    IS_DEV = True


configMap = {
    "development": DevConfig,
    "production": ProdConfig,
    "default": DevConfig
}

config = configMap[os.getenv('AUTOAUTO_CONFIG') or "default"]

__all__ = ["config"]
