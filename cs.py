#!/usr/bin/env python

import glob
#  import pprint
#  import tomllib

import click

from tabulate import tabulate

DEBUG = False
#  del(DEBUG)

CHEATSHEETS_PATH = "./hotkeys/*.xx"
OUTPUT_PATH = "./output"

try:
    import config as cfg
except ImportError:
    pass
else:
    if not DEBUG:
        CHEATSHEETS_PATH = cfg.CHEATSHEETS_PATH
        OUTPUT_PATH = cfg.OUTPUT_PATH

TABLE_HEADERS = ["Action", "Hotkeys"]


class Cheatsheeter:
    def __init__(self, cheatsheets_path, output_path):

        self.cheatsheets_path = cheatsheets_path
        self.output_path = output_path

        files = self.get_cheatsheet_files(cheatsheets_path)
        self.files = files

        cheatsheets_dict = self.get_cheatsheet_dict(files)
        self.cheatsheets_dict = cheatsheets_dict

        self.read_cheatsheets(cheatsheets_dict=cheatsheets_dict)

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

    def read_cheatsheets(self, cheatsheets_dict=None, verbose=False):

        if not cheatsheets_dict:
            cheatsheets_dict = self.cheatsheets_dict

        cheatsheets = dict()

        for program, filepath in cheatsheets_dict.items():

            if verbose:
                print(f"Reading file '{filepath}'.")

            with open(filepath, "r") as cheetsheet_fd:
                cheatsheet = cheetsheet_fd.read()

            entries = [entry.strip()
                       for entry in cheatsheet.split("\n\n") if entry.strip()]

            cheatsheets.update({program: entries})

        self.cheatsheets = cheatsheets

    def write_output_file(self, output_path, program_name, data, verbose):
        output_file_path = self.get_output_file_path(output_path=output_path,
                                                     program_name=program_name)

        if verbose:
            print(f"Writing file '{output_file_path}'.")

        with open(output_file_path, "w") as output_file:
            output_file.write(data)

        return output_file_path

    def write_files(self, cheatsheets=None, output_path=None, verbose=False):

        if not cheatsheets:
            cheatsheets = self.cheatsheets

        if not output_path:
            output_path = self.output_path

        for program, entries in cheatsheets.items():
            hotkey_list = list()

            for entry in entries:
                action, hotkeys = entry.strip('\n').split('\n', maxsplit=1)
                keys = " + ".join([f"<kbd>{key.title()}</kbd>"
                                   for key in hotkeys.split(' ') if key])
                hotkey_list.append([action, keys])

            tb = tabulate(tabular_data=hotkey_list, headers=TABLE_HEADERS,
                          tablefmt="github")

            self.write_output_file(output_path=output_path,
                                   program_name=program,
                                   data=tb,
                                   verbose=verbose)

    def print_cheatsheets(self, cheatsheets=None):

        if not cheatsheets:
            cheatsheets = self.cheatsheets

        for program, entries in cheatsheets.items():
            hotkey_list = list()

            for entry in entries:
                action, hotkeys = entry.strip('\n').split('\n', maxsplit=1)
                keys = " + ".join([f"{key.title()}"
                                   for key in hotkeys.split(' ')
                                   if key.strip()])
                hotkey_list.append([action, keys])

            tb = tabulate(tabular_data=hotkey_list, headers=TABLE_HEADERS,
                          tablefmt="rounded_grid")
            print(program, tb, sep="\n", end="\n\n")

#  @click.group(invoke_without_command=True)
#  def cheatsheeter(ctx):
#      pass

#  @click.command
#  @click.option("-p", "--print", is_flag=True)
#  @click.group(invoke_without_command=True)
#  @click.group()
#  @click.pass_context
#  def cheatsheeter(ctx):
@click.group()
def cheatsheeter():
    pass
    #  if ctx.invoked_subcommand is None:
    #      cs = Cheatsheeter(cheatsheets_path=CHEATSHEETS_PATH,
    #                        output_path=OUTPUT_PATH)  # FIXME: we don't need this
    #                                                  # for printing only
    #
    #      if print:
    #          cs.print_cheatsheets()
    #      else:
    #          cs.write_files(verbose=True)

@cheatsheeter.command(name="list")
def list_cmd():
    cs = Cheatsheeter(cheatsheets_path=CHEATSHEETS_PATH,
                      output_path=OUTPUT_PATH)

    cheatsheet_list = "\n".join(cs.cheatsheets_dict.keys())
    #  print(f"Available cheatsheets matching '{cs.cheatsheets_path}':", end="\n\n")
    print(cheatsheet_list)

@cheatsheeter.command(name="print")
def print_cmd():
    cs = Cheatsheeter(cheatsheets_path=CHEATSHEETS_PATH,
                      output_path=OUTPUT_PATH)

    cs.print_cheatsheets()

@cheatsheeter.command(name="write")
def write_cmd():
    cs = Cheatsheeter(cheatsheets_path=CHEATSHEETS_PATH,
                      output_path=OUTPUT_PATH)

    cs.print_cheatsheets()


if __name__ == "__main__":
    cheatsheeter()
