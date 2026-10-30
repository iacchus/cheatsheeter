#!/usr/bin/env python

import glob
import tomllib

CHEATSHEETS_PATH = "./hotkeys/*.xx"

files = glob.glob(CHEATSHEETS_PATH)

print(files)
