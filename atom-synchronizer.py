#!/usr/bin/python
# coding=utf-8

import argparse
import re
import os
import shutil

cliParser = argparse.ArgumentParser("""
Backup/restore atom configurations to/form other machines.
""")
cliParser.add_argument("action",
                       help="""
                       The action to do
                       Must be one of 'backup' or 'restore'
                       """)
cliParser.add_argument("-a",
                       "--atomDir",
                       default='~/.atom',
                       help="""
                       The directory path of your '.atom'
                       defual '~/.atom'
                       """)
cliParser.add_argument("-b",
                       "--backupDir",
                       default='.',
                       help="""
                       The directory path for backup files
                       defualt '.'
                       """)
cliParser.add_argument("-p",
                       "--packagelist",
                       default='packagelist.txt',
                       help="""
                       Package list file name to load from or save to
                       default= {backup-floder}/packagelist.txt
                       """)
cliParser.add_argument("-k",
                       "--keepVersion",
                       action="store_true",
                       default=False,
                       help="""
                       Keep same package version
                       default=False
                       """)


def parsePackages(packageListPath, withVersion):
    if packageListPath:
        fileContent = open(packageListPath).read()
        userPS = re.compile(r'\n(.*packages\[.*).*').findall(fileContent)[0]
        userPSStr = fileContent.split(userPS)[1]
        pacagesWithVersion = re.compile(r'├── (.*@.*)\n').findall(userPSStr)
        if withVersion:
            return pacagesWithVersion
        else:
            pacagesNoVersion = []
            for p in pacagesWithVersion:
                pkg = re.compile(r'(.*)@.*').findall(p)[0]
                pacagesNoVersion.append(pkg)
            return pacagesNoVersion

args = cliParser.parse_args()


# Backup configurations and packages list
def backup():
    # backup package list
    pkglistpath = args.packagelist
    if not os.path.isfile(pkglistpath):
        pkglistpath = args.backupDir + '/' + args.packagelist
    os.system("apm list > " + pkglistpath)
    if os.path.isdir(args.atomDir):
        for f in os.listdir(args.atomDir):
            sfile = args.atomDir+'/'+f
            if os.path.isfile(sfile):
                shutil.copyfile(sfile, args.backupDir+'/' + f)


# Restore configuration and packages
def restore():
    # restore configs
    if os.path.isdir(args.atomDir):
        for f in os.listdir(args.backupDir):
            sfile = args.backupDir+'/'+f
            if os.path.isfile(sfile):
                shutil.copyfile(sfile, args.atomDir+'/' + f)
    # restore packages
    pkglistpath = args.packagelist
    if not os.path.isfile(pkglistpath):
        pkglistpath = args.backupDir + '/' + pkglistpath
    if os.path.isfile(pkglistpath):
        packages = parsePackages(pkglistpath, args.keepVersion)
        for p in packages:
            os.system("apm install " + p)
    else:
        raise("package list file not found!")


if __name__ == '__main__':
    if args.action == 'backup':
        backup()
    elif args.action == 'restore':
        restore()
