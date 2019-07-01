#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import string
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))  # noqa
from git import Repo, Git
from git.exc import InvalidGitRepositoryError
from common_utils import repo_service
import stat
import logging
import subprocess
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def checkversion(lib):
    lib_path=str(Path.home())+"/.cocoapods/repos/citrite-citrix-cocoapods/"
    cwd=os.path.join(lib_path,str(lib))
    command='ls -t'
    versions_list=subprocess.check_output(command, universal_newlines=True, shell=True, cwd=cwd)
    return versions_list.split()


# system(command) -> exit_status
# Execute the command (a string) in a subshell.
def PodfileupdateToLatest(podfilePath):
    fileread = open(podfilePath, "r")
    flist = fileread.readlines()
    fileread.close()
    filehandle=open(podfilePath, "w")
    EditFlag=False
    for line in flist:
        podlib=line.strip()
        if podlib.startswith('def common_app_target_pods') or line.startswith('def intune_app_target_pods'):
            EditFlag=True
        if podlib.startswith('end'):
            EditFlag=False
        if podlib.startswith('pod') and EditFlag:
            lib = ''.join(ch for ch in podlib if ch not in ["\'",","])
            lib=lib.split()
            print("Package name and current version: %s, %s\n"%(lib[1],lib[2]))
            logger.info("Package name and current version: %s, %s\n"%(lib[1],lib[2]))
            #print(lib[1])
            if lib[1]!='g11n_sdk_ios' and lib[1] != 'CitrixLoggerFramework':
                versions= checkversion(lib=lib[1])
                print("Avalible version: %s"%(versions))
                print("Latest version: %s"%(versions[0]))
                logger.info("Avalible version: %s"%(versions))
                logger.info("Latest version: %s"%(versions[0]))
                podinfo = "    pod '%s', '=%s'\n"%(lib[1], versions[0])
                line = podinfo
        filehandle.write(line)
    filehandle.close()

def PodfileupdateToCurrentLatest(podfilePath):
    fileread = open(podfilePath, "r")
    flist = fileread.readlines()
    fileread.close()
    filehandle=open(podfilePath, "w")
    EditFlag=False
    for line in flist:
        podlib=line.strip()
        if podlib.startswith('def common_app_target_pods') or line.startswith('def intune_app_target_pods'):
            EditFlag=True
        if podlib.startswith('end'):
            EditFlag=False
        if podlib.startswith('pod') and EditFlag:
            lib = ''.join(ch for ch in podlib if ch not in ["\'",","])
            lib=lib.split()
            if lib[1]!='g11n_sdk_ios' and lib[1] != 'CitrixLoggerFramework':
                podinfo = "    pod '%s', '~>%s'\n"%(lib[1], lib[2])
                line = podinfo
        filehandle.write(line)
    filehandle.close()

def PodFileContents(podfilePath, isOverride, **libInfo):
    info = ''
    for libName in libInfo.keys():
        if libInfo[libName] == '0':  # 用户输入时，0代表缺省属性，即不指定库的版本号
            podInfo = "pod '%s'\n" % (libName)
        elif libInfo[libName] == 'no':  # 用户输入q时，表示什么都不用
            podInfo = ' '
        else:
            podInfo = "pod '%s', '~> %s'\n" % (libName, libInfo[libName])
        
        info += podInfo
    
    if isOverride == 'o':
        iosVersion = raw_input('Please enter iOS version: \n')
        iosVersion.strip()
        content = "platform:ios, '%s'\n" % iosVersion
        content += info
        filehandle = open(podfilePath, "w")
        filehandle.write(content)
        filehandle.close()
    else:
        filehandle = open(podfilePath, "a")
        filehandle.write(info)
        filehandle.close()

def generatePodfile(filepath, projectpath, isoverride):
    libInfo = getUserInputLibInfo()
    PodFileContents(filepath, isoverride, **libInfo)
    os.chdir(projectpath)
    print  ('====== podfile log ======')
    os.system('pod install --verbose --no-repo-update')


# 判断给定路径的文件夹下是否包含某后缀名的文件，返回BOOL类型
def isAvailablePath(path, extension, isOpen):
    # 先判断给定路径的合法性
    path = path.strip()
    if os.path.exists(path):
        pathList = os.listdir(path)
        for fileName in pathList:
            if fileName.endswith(extension):
                filepath = path + '/%s' % fileName
                if isOpen == True:
                    os.system('open %s' % filepath)
                return True
        # 出循环，表示没有搜到这个文件
        return False
    else:
        return False


def check_and_update(project_name, latestFlag):
    # 获取工程文件夹路径
    projectPath = repo_service.get_code_dir(project_name)
    result = isAvailablePath(projectPath, 'xcodeproj', False)  # verify the project path
    
    while result != True:
        projectPath = logger.info("there is no Secure mail project!")
        result = isAvailablePath(projectPath, 'xcodeproj', False)

    projectPath = projectPath.strip()
    filePath = projectPath + '/Podfile'
    if latestFlag:
       PodfileupdateToLatest(filePath)
    else:
       PodfileupdateToCurrentLatest(filePath)



