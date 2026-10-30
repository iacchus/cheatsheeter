#!/usr/bin/env python

import glob
import pprint
import tomllib

from tabulate import tabulate

CHEATSHEETS_PATH = "./hotkeys/*.xx"
TABLE_HEADERS = ["Action", "Hotkeys"]

files = glob.glob(CHEATSHEETS_PATH)

print(files)

cheatsheets_dict = {entry.split('/')[-1].split('.')[0]: entry for entry in files}

print(cheatsheets_dict)

data = dict()

for program, filepath in cheatsheets_dict.items():
    hotkey_list = list()
    with open(filepath, "r") as cheetsheet_fd:
        #  cheatsheet = cheetsheet_fd.readlines()
        cheatsheet = cheetsheet_fd.read()

    entries = cheatsheet.split("\n\n")

    for entry in entries:
        action, hotkeys = entry.strip('\n').split('\n', maxsplit=1)
        hotkey_list.append([action, hotkeys])
    #  data.update({f"{program}": for entry in entries})

    data.update({program: hotkey_list})

    tb = tabulate(tabular_data=hotkey_list, headers=TABLE_HEADERS, tablefmt="github")
    print(tb)
    #  table = tabulate(table=hotkey_list, headers=TABLE_HEADERS, tablefmt="github")

    #  print(hotkey_list)
    #  print(cheatsheet)
    #  print(cheatsheet.split("\n\n"))
pprint.pprint(data)
