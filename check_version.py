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
logger = logging.getLogger()

def checkversion(lib):
    lib_path=str(Path.home())+"/.cocoapods/repos/citrite-citrix-cocoapods/"
    cwd=os.path.join(lib_path,str(lib))
    command='ls -t'
    versions_list=subprocess.check_output(command, universal_newlines=True, shell=True, cwd=cwd)
    return versions_list.split()


# system(command) -> exit_status
# Execute the command (a string) in a subshell.
def Podfileupdate(podfilePath):
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
            logger.info("name and current version: %s, %s\n"%(lib[1],lib[2]))
            print(lib[1])
            if lib[1]!='g11n_sdk_ios' and lib[1] != 'CitrixLoggerFramework':
                versions= checkversion(lib=lib[1])
                logger.info("avalible version: %s"%(versions))
                print(versions)
                podinfo = "    pod '%s', '=%s'\n"%(lib[1], versions[0])
                line = podinfo
        filehandle.write(line)
    filehandle.close()




def PodFileContents(podfilePath, isOverride, **libInfo):
    info = ''
    for libName in libInfo.keys():
        if libInfo[libName] == '0':
            podInfo = "pod '%s'\n" % (libName)
        elif libInfo[libName] == 'no':
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


def isAvailablePath(path, extension, isOpen):
    path = path.strip()
    if os.path.exists(path):
        pathList = os.listdir(path)
        for fileName in pathList:
            if fileName.endswith(extension):
                filepath = path + '/%s' % fileName
                if isOpen == True:
                    os.system('open %s' % filepath)
                return True
        return False
    else:
        return False


def check_and_update(project_name):
    projectPath = repo_service.get_code_dir(project_name)  #
    result = isAvailablePath(projectPath, 'xcodeproj', False)
    
    while result != True:
        projectPath = logger.info("there is no Secure mail project!")
        result = isAvailablePath(projectPath, 'xcodeproj', False)

    projectPath = projectPath.strip()
    filePath = projectPath + '/Podfile'
    Podfileupdate(filePath)



