#!/usr/bin/env python

import glob
import pprint
#  import tomllib

import click

from tabulate import tabulate

DEBUG = True

try:
    import config as cfg
except ImportError:
    CHEATSHEETS_PATH = "./hotkeys/*.xx"
    OUTPUT_PATH = "./output"
else:
    if not DEBUG:
        CHEATSHEETS_PATH = cfg.CHEATSHEETS_PATH
        OUTPUT_PATH = cfg.OUTPUT_PATH
    else:
        CHEATSHEETS_PATH = "./hotkeys/*.xx"
        OUTPUT_PATH = "./output"

TABLE_HEADERS = ["Action", "Hotkeys"]


class Cheatsheeter:
    def __init__(self, cheatsheets_path, output_path):

        self.cheatsheets_path = cheatsheets_path
        self.output_path = output_path

        files = self.get_cheatsheet_files(cheatsheets_path)
        self.files = files

        cheatsheets_dict = self.get_cheatsheet_dict(files)
        self.cheatsheets_dict = cheatsheets_dict

        #  self.write_files(cheatsheets_dict=cheatsheets_dict,
        #                   output_path=output_path)

    def get_cheatsheet_files(self, cheatsheet_path):
        files = glob.glob(cheatsheet_path)
        return files

    def get_cheatsheet_dict(self, files):
        cheatsheets_dict = {entry.split('/')[-1].split('.')[0]:
                            entry for entry in files}
        return cheatsheets_dict

    def get_output_file_path(self, output_path, program_name):
        output_file_path = f"{output_path}/{program_name}.md"
        return output_file_path

    def write_output_file(self, output_path, program_name, data):
        output_file_path = self.get_output_file_path(output_path=output_path,
                                                     program_name=program_name)

        with open(output_file_path, "w") as output_file:
            output_file.write(data)

        return output_file_path

    def read_cheatsheets(self, cheatsheets_dict):

        if not cheatsheets_dict:
            cheatsheets_dict = self.cheatsheets_dict

        cheatsheets = dict()

        for program, filepath in cheatsheets_dict.items():
            hotkey_list = list()

            with open(filepath, "r") as cheetsheet_fd:
                cheatsheet = cheetsheet_fd.read()

            entries = [entry.strip()
                       for entry in cheatsheet.split("\n\n") if entry]

            for entry in entries:
                action, hotkeys = entry.strip('\n').split('\n', maxsplit=1)
                keys = " + ".join([f"<kbd>{key.title()}</kbd>"
                                   for key in hotkeys.split(' ') if key])
                hotkey_list.append([action, keys])

            cheatsheets.update({program: hotkey_list})

        self.cheatsheets = cheatsheets

    def write_files(self, cheatsheets_dict=None, output_path=None):

        if not cheatsheets_dict:
            cheatsheets_dict = self.cheatsheets_dict

        if not output_path:
            output_path = self.output_path

        cheatsheets = dict()

        for program, filepath in cheatsheets_dict.items():
            hotkey_list = list()

            with open(filepath, "r") as cheetsheet_fd:
                cheatsheet = cheetsheet_fd.read()

            entries = [entry.strip()
                       for entry in cheatsheet.split("\n\n") if entry]

            for entry in entries:
                action, hotkeys = entry.strip('\n').split('\n', maxsplit=1)
                keys = " + ".join([f"<kbd>{key.title()}</kbd>"
                                   for key in hotkeys.split(' ') if key])
                hotkey_list.append([action, keys])

            cheatsheets.update({program: hotkey_list})

            tb = tabulate(tabular_data=hotkey_list, headers=TABLE_HEADERS,
                          tablefmt="github")
            #  print(tb)

            self.write_output_file(output_path=output_path,
                                   program_name=program,
                                   data=tb)

        #  pprint.pprint(data)
        pprint.pprint(cheatsheets)

    def print_cheatsheets(self, cheatsheets=None):
    #  def print_cheatsheets(self, cheatsheets_dict=None, output_path=None):

        if not cheatsheets:
            cheatsheets = self.cheatsheets

        #  if not output_path:
        #      output_path = self.output_path

        #  cheatsheets = dict()
        for program, filepath in cheatsheets_dict.items():
            hotkey_list = list()

            with open(filepath, "r") as cheetsheet_fd:
                cheatsheet = cheetsheet_fd.read()

            entries = [entry.strip()
                       for entry in cheatsheet.split("\n\n") if entry]

            for entry in entries:
                action, hotkeys = entry.strip('\n').split('\n', maxsplit=1)
                keys = " + ".join([f"<kbd>{key.title()}</kbd>"
                                   for key in hotkeys.split(' ') if key])
                hotkey_list.append([action, keys])

            cheatsheets.update({program: hotkey_list})

            tb = tabulate(tabular_data=hotkey_list, headers=TABLE_HEADERS,
                          tablefmt="rounded_grid")
            print(program, tb, sep="\n", end="\n\n")

        #  for program, filepath in cheatsheets_dict.items():
        #      hotkey_list = list()
        #
        #      with open(filepath, "r") as cheetsheet_fd:
        #          cheatsheet = cheetsheet_fd.read()
        #
        #      entries = [entry.strip()
        #                 for entry in cheatsheet.split("\n\n") if entry]
        #
        #      for entry in entries:
        #          action, hotkeys = entry.strip('\n').split('\n', maxsplit=1)
        #          keys = " + ".join([f"<kbd>{key.title()}</kbd>"
        #                             for key in hotkeys.split(' ') if key])
        #          hotkey_list.append([action, keys])
        #
        #      cheatsheets.update({program: hotkey_list})
        #
        #      tb = tabulate(tabular_data=hotkey_list, headers=TABLE_HEADERS,
        #                    tablefmt="rounded_grid")
        #      print(program, tb, sep="\n", end="\n\n")

            #  self.write_output_file(output_path=output_path,
            #                         program_name=program,
            #                         data=tb)

        #  pprint.pprint(data)
        self.cheatsheets = cheatsheets
        pprint.pprint(cheatsheets)

#  @click.group
#  def cli():
#      pass

@click.command
@click.option("--print", is_flag=True)
def cheatsheeter(print):
    cs = Cheatsheeter(cheatsheets_path=CHEATSHEETS_PATH,
                      output_path=OUTPUT_PATH)

    if print:
        cs.print_cheatsheets()
    else:
        cs.write_files()

if __name__ == "__main__":
    cheatsheeter()
