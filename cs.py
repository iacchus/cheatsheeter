#!/usr/bin/env python

import glob
import tomllib

CHEATSHEETS_PATH = "./hotkeys/*.xx"

files = glob.glob(CHEATSHEETS_PATH)

print(files)

cheatsheets_dict = {entry.split('/')[-1].split('.')[0]: entry for entry in files}

print(cheatsheets_dict)

for item, filepath in cheatsheets_dict.items():
    with open(filepath, "r") as cheetsheet_fd:
        #  cheatsheet = cheetsheet_fd.readlines()
        cheatsheet = cheetsheet_fd.read()

    print(cheatsheet)
    print(cheatsheet.split("\n\n"))
