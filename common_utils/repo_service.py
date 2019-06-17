from git import Repo, Git
from git.exc import InvalidGitRepositoryError
from common_utils import utils
from retrying import retry
import os
import stat
import logging

from config import config
logger = logging.getLogger()

# secure-mail code path
def get_code_dir(component_name):
    code_dir = os.path.join(
        config.BASE_DIR,
        str(component_name)
    )
    return code_dir


def _git_ssh_command():
    # we should ensure the identity file permission is 600
    git_ssh_identity_file = os.path.join(
        os.path.dirname(__file__),
        "ssh_wrapper")
    os.chmod(git_ssh_identity_file, stat.S_IRUSR)
    # disable add to know_host promote
    git_ssh_cmd = 'ssh -o StrictHostKeyChecking=no -i %s'\
        % git_ssh_identity_file
    return git_ssh_cmd


def clone_repo(repo_url, code_dir):  # 测试代码不存在，克隆repo_url的代码到本地code_dir目录
    utils.remove_dir(code_dir)
    logger.info("Download repo at:%s from: %s" % (code_dir, repo_url))
    # with Git().custom_environment(GIT_SSH_COMMAND=_git_ssh_command()):
    env = {"GIT_SSH_COMMAND": _git_ssh_command()}
    Repo.clone_from(repo_url, code_dir, env=env)
    logger.info('repo downloaded at:' + code_dir)


def pull_repo(code_dir):  #d测试代码已存在，pull
    repo = Repo(code_dir)
    with repo.git.custom_environment(GIT_SSH_COMMAND=_git_ssh_command()):
        logger.info("pull latest code at:%s", code_dir)
        try:
            repo.git.pull("--force")
        except InvalidGitRepositoryError as error:
            raise error
        except Exception as error:
            logger.exception(error)

@retry(wait_fixed=3000, stop_max_attempt_number=2)
def change_to_branch(code_dir, new_branch_name):
    repo = Repo(code_dir)
    with repo.git.custom_environment(GIT_SSH_COMMAND=_git_ssh_command()):
        logger.info("pull latest code at:%s", code_dir)
        try:
            repo.git.checkout(new_branch_name)
        except InvalidGitRepositoryError as error:
            raise error
        except Exception as error:
            logger.exception(error)


def fetch_code(repo_url, component_name, repo_branch=None):
    code_dir = get_code_dir(component_name) #automation代码的本地repo的位置
    if os.path.exists(code_dir):
        try:
            pull_repo(code_dir)
        except InvalidGitRepositoryError as error:
            logger.info("invalid git repo error catched, will do clone option")
            clone_repo(repo_url, code_dir)
    else:
        utils.ensure_dir(code_dir)
        clone_repo(repo_url, code_dir)
    if repo_branch:
        change_to_branch(code_dir, repo_branch)
        logger.info('change to branch %s', repo_branch)
    return code_dir


def ensure_branch(component_name, repo_branch=None):
    code_dir = get_code_dir(component_name)
    change_to_branch(code_dir, repo_branch)
