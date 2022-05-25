#!/usr/bin/env python3
import os

project_path = "~/projects/learning/devops-16/"
bash_command = ["cd " + project_path, "git status"]

result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = os.path.join(os.path.expanduser(project_path), result.replace('\tmodified:   ', ''))
        is_change = True
        print(prepare_result)
if is_change != True:
    print('No modified files')