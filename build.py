#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))  # noqa

import time
import logging.config
from config import config as Config
from multiprocessing import Process
from xcodebuild.test_suites import append_command as testcase_ids
from xcodebuild.test_suites import Testsuites
from xcrun import simctl
import simctl_service
from common_utils import repo_service
import check_version
import subprocess
import json
from retrying import retry
import logging
logger = logging.getLogger()


class BuildFaildException(Exception):
    """Raised when build failed"""
    pass
def get_build_config(cwd):
    command = 'xcodebuild -list -json'
    result = subprocess.check_output(command, universal_newlines=True, shell=True, cwd=cwd)
    config = json.loads(result)
    return config

def _run_command(command, cwd):
    # Deliberately don't catch the exception - we want it to bubble up
    print (command)
    print(cwd)
    return subprocess.call(command,
                           universal_newlines=True,
                           shell=True,
                           cwd=cwd)


@retry(retry_on_exception=lambda e: isinstance(e, BuildFaildException),
       stop_max_attempt_number=3,
       wait_fixed=2000)

def _run_build_command(scheme, device_id, test_locale, cwd,
                       report_dir):

    prefix = ' -only-testing:'
    append_command = testcase_ids
    log_path = os.path.join(report_dir, "report.log")
    try:
        os.makedirs(os.path.dirname(log_path))
    except FileExistsError as e:
        pass

    full_command = 'xcodebuild test \
                        -scheme {0} \
                        -destination "id={1}" \
                        -testLanguage {2} \
                        {3}\
                            | tee {4}'.format(
        scheme,
        device_id,
        test_locale,
        append_command,
        log_path)
    logger.info("run build command: %s", full_command)
    result = _run_command(full_command, cwd)



def run_test(instance_id, scheme, device_id, test_locale, cwd):
    report_dir = os.path.join(Config.BASE_DIR,Config.REPORT_SAVE_RELATIVE_PATH,str(instance_id))
    return _run_build_command(scheme,
                              device_id,
                              test_locale,
                              cwd,
                              report_dir)

def do_test():
    #do configure, about simulator info and source code repo address
    instance_id = 15
    locale = 'en'
    device_type = 'iPhone X'
    component_name = 'sm-automation'
    project_name = 'secure-mail'
    source_code_repo = 'ssh://git@blr-lcy2-code.citrite.net:7999/code/xmios/secure-mail.git'
    test_repo = 'ssh://git@code.citrite.net/gsrv/gs-automation-secure-mail-ios.git'
    logger.info("Download repo from: %s" % (source_code_repo))
    
    #download from remote repo
    #repo_service.fetch_code(test_repo, component_name)  #参数，远程仓库url和项目名称
    #repo_service.fetch_code(source_code_repo, project_name)
    wm_repo_path=repo_service.get_code_dir(project_name)
    report_dir = os.path.join(Config.BASE_DIR,Config.REPORT_SAVE_RELATIVE_PATH,str(instance_id))
    #remote_branch_name = ' origin/Feature_CXM-53041-slack-tp2'
    #local_branch_name = ' Feature_CXM-53041-slack-tp2'
    #_run_command('git checkout .',wm_repo_path)
    #checkout_branch_command = 'git checkout -b'+local_branch_name+remote_branch_name
    #_run_command(checkout_branch_command,wm_repo_path)
    #repo_service.pull_repo(source_code_repo)
    
    _run_command('pod install', wm_repo_path)
    check_version.check_and_update(project_name)  #packeges_version_check_and_update
    _run_command('pod install --verbose --no-repo-update | tee {0}'.format(report_dir), wm_repo_path)
    config = get_build_config(wm_repo_path)       # create new wm build with updated pancages
    wm_scheme = config.get('project').get('schemes')[4]      # 4enterprise 5worxmailpush
    wm_workspace = config.get('project').get('name')+'.xcworkspace'
    
    create_command = 'xcodebuild -workspace {0} -scheme {1} -configuration Debug -sdk iphonesimulator12.1 -derivedDataPath . | tee {2}'.format(wm_workspace,wm_scheme,report_dir)
    logger.info("run build command: %s", create_command)
    
    _run_command(command=create_command,cwd=wm_repo_path)
    app_relative_path = '/Build/Products/Debug-iphonesimulator/'+wm_scheme+'.app'
    app_path = wm_repo_path+app_relative_path
    
    #test   app_path = '/Users/shuzhenli/Code/secure-mail/Build/Products/Debug-iphonesimulator/WorxMailEnterprise.app'
    
    new_device_name = '%s_%d_%s' % (device_type, instance_id, locale)    #create a new simulator
    device = simctl_service.create_and_boot_simulator(new_device_name, device_type)
    logger.info('successfully create simulator'+new_device_name)
    
    simctl.install_app(device, app_path)     #install the build app
    logger.info('app installed at:' + app_path)
    auto_repo_path=repo_service.get_code_dir(component_name)
    # run test
    
    scheme='SecureMailG11nAutomation'
    target='SecureMailUITests'
    run_test(instance_id=instance_id,scheme=scheme,device_id=device.udid,test_locale=locale,cwd=auto_repo_path)
    logger.info('tests run complete')
    
# delete the simulator device
    try:
        simctl_service.delete_simulator(device)
    except Exception as error:
        logger.warning("Delete simulator: %s faild", device.name)
        logger.exception(error)


if __name__ == "__main__":
    #do_test()
    test_suites = TestSuites(path='/Users/yangwa/Automation/secure-web-automation'  cases = ['GSTC-16570', 'GSTC-16578', 'GSTC-16578']
                             # target = 'SecureWebUITest'
                             # test_suites.filter_case_id_by_list(target, cases)
    prefix = ' -only-testing:'
    append_command = prefix + prefix.join(testcase_ids)
    print(append_command)
    '''
    app_path = '/Users/shuzhenli/Code/secure-mail/Build/Products/Debug-iphonesimulator/WorxMailEnterprise.app'
    locale = 'en'
    device_type = 'iPhone X'
    component_name = 'sm-automation'
    instance_id = '15'
    new_device_name = '%s_%s' % (device_type, locale)    #create a new simulator
    device = simctl_service.create_and_boot_simulator(new_device_name, device_type)
    logger.info('successfully create simulator'+new_device_name)
    auto_repo_path=repo_service.get_code_dir(component_name)
    simctl.install_app(device, app_path)     #install the build app
    logger.info('app installed at:' + app_path)
    scheme='SecureMailG11nAutomation'
    target='SecureMailUITests'
    run_test(instance_id=instance_id,scheme=scheme,device_id=device.udid,test_locale=locale,cwd=auto_repo_path)
    logger.info('tests run complete')
    '''
