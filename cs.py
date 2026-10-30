#!/usr/bin/env python

import glob
#  import pprint
#  import tomllib

from tabulate import tabulate

CHEATSHEETS_PATH = "./hotkeys/*.xx"
OUTPUT_PATH = "./output"
TABLE_HEADERS = ["Action", "Hotkeys"]

files = glob.glob(CHEATSHEETS_PATH)

#  print(files)

cheatsheets_dict = {entry.split('/')[-1].split('.')[0]: entry for entry in files}

#  print(cheatsheets_dict)

data = dict()

for program, filepath in cheatsheets_dict.items():
    hotkey_list = list()
    with open(filepath, "r") as cheetsheet_fd:
        cheatsheet = cheetsheet_fd.read()

    entries = cheatsheet.split("\n\n")

    for entry in entries:
        action, hotkeys = entry.strip('\n').split('\n', maxsplit=1)
        keys = " + ".join([f"<kbd>{key.title()}</kbd>" for key in hotkeys.split(' ') if key])
        #  hotkey_list.append([action, hotkeys])
        hotkey_list.append([action, keys])

    data.update({program: hotkey_list})

    tb = tabulate(tabular_data=hotkey_list, headers=TABLE_HEADERS, tablefmt="github")
    print(tb)

    with open(f"{OUTPUT_PATH}/{program}.md", "w") as output_file:
        output_file.write(tb)

#  pprint.pprint(data)
