#!/usr/bin/env python3
import os
import sys
import subprocess

arguments = sys.argv

if len(arguments) <= 1:
    print("Empty path argument")
    exit(1)

if arguments[1].replace(" ", "") == '':
    print("Empty string in path argument")
    exit(1)

project_path = arguments[1]

if os.path.isdir(project_path) != True:
    print("Path is not a directory")
    exit(1)

git_status_command = subprocess.Popen(['git', 'status'], cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
git_status_command.wait()

if git_status_command.returncode != 0:
    print("Git repo not found in a directory")
    exit(1)

result_os = git_status_command.stdout.read().decode("utf-8").rstrip()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = os.path.join(project_path, result.replace('\tmodified:   ', ''))
        is_change = True
        print(prepare_result)
if is_change != True:
    print('No modified files')
    