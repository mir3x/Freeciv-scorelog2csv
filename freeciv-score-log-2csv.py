#!/usr/bin/env python3

# freeciv-score-log.py, a script to make some csv:s out of freeciv-score.log
# Copyright (C) 2003 Ragnar Ouchterlony
# Copyright (C) 2015 Louis Moureaux
# Copyright (C) 2020 mir3x
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import sys
import traceback
from argparse import ArgumentParser

class scorelog_reader:
    def __init__(self, file_name):
        self.filename = file_name
        self.fcId = ""
        self.fcTags = {}
        self.fcTurns = {}
        self.fcPlayers = {}
        self.fcData = {}
        self.tagLimit = []

    def _set_id(self, args):
        self.fcId = args.strip()

    def _set_tag(self, args):
        tid, descr = str.split(args, maxsplit=1)
        tid = int(tid)
        self.fcTags[tid] = descr

    def _set_turn(self, args):
        turn, num, descr = str.split(args, maxsplit=2)
        turn = int(turn)
        num = int(num)
        descr = descr.strip()
        self.fcTurns[turn] = (num, descr)


    def _add_player(self, args):
        turn, pid, name = str.split(args, maxsplit=2)
        turn = int(turn)
        pid = int(pid)
        name = name.strip()
        if pid in self.fcPlayers:
            self.fcPlayers[pid][1].append((turn, None))
        else:
            self.fcPlayers[pid] = (name, [(turn, None)])
        print("Added player: ", name,)

    def _del_player(self, args):
        turn, pid = str.split(args, maxsplit=1)
        turn = int(turn)
        pid = int(pid)
        if pid in self.fcPlayers:
            begTurn = self.fcPlayers[pid][1][-1][0]
            self.fcPlayers[pid][1][-1] = (begTurn, turn)
        else:
            print("Can't delete nonexisting player.")

    def _set_data(self, args):
        turn, tid, pid, value = str.split(args, maxsplit=3)
        turn = int(turn)
        tid = int(tid)
        pid = int(pid)
        value = float(value)

        if tid not in self.fcData:
            self.fcData[tid] = {}
        if turn not in self.fcData[tid]:
            self.fcData[tid][turn] = {}
        self.fcData[tid][turn][pid] = value

    def _invalid(self, args):
        pass

    def load_scorelog(self):
        firstTurn = 0
        lastTurn = 0
        func_dict = {
                    'id'         : self._set_id,
                    'tag'        : self._set_tag,
                    'turn'       : self._set_turn,
                    'addplayer'  : self._add_player,
                    'delplayer'  : self._del_player,
                    'data'       : self._set_data }
        try:
            with open(self.filename, "r") as reader:
                whole_file = reader.readlines()

                while whole_file:
                    line = whole_file.pop(0)

                    if line[0] in ['\n', "#"]:
                        continue

                    lastTurn += 1
                    line = line.strip()
                    command, args = str.split(line, maxsplit=1)
                    args = args.strip()
                    func_dict.get(command, self._invalid)(args)
                    lastTurn += 1
                    line = line.strip()

            reader.close()

        except:
            err = sys.exc_info()[0]
            print(f"\033[91mError ***{err}*** when reading file {self.filename}. Exiting\033[0m")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            exit(1)

        return self.fcTags, self.fcData, self.fcPlayers, self.fcId, self.tagLimit, firstTurn, lastTurn

def make_directory(fcId):
    try:
        if not os.path.exists(fcId):
            os.makedirs(fcId)
    except OSError as e:
        err = sys.exc_info()[0]
        print(f"Error when creating directory: ***{err}***. Exiting")
        exit(1)

def write_csv(fcTags, fcData, fcPlayers, fcId, taglimit, firstTurn, lastTurn):

    for tid in fcTags.keys():

        if taglimit and fcTags[tid] not in taglimit:
            continue

        filename = f"{fcTags[tid]}.csv"
        out = None
        try:
            with open(f'{fcId}/{filename}', 'w') as out:

                # Header
                out.write("\"turn\",")
                for pid in fcPlayers.keys():
                    out.write("\"%s\"," % fcPlayers[pid][0])
                out.write("\n")

                # Data
                for turn in range(firstTurn, lastTurn):
                    if turn in fcData[tid]:
                        out.write("%d," % turn)
                        for pid in fcPlayers.keys():
                            if pid in fcData[tid][turn]:
                                out.write("%d," % fcData[tid][turn][pid])
                            else:
                                out.write(",")
                        out.write("\n")
                print(f"{filename } written")
        except:
            err = sys.exc_info()[0]
            print(f"\033[91mError ***{err}*** when writing file {filename}\033[0m")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

        finally:
            out.close()


def main(filename, outdir):

    sc = scorelog_reader(filename)
    [fcTags, fcData, fcPlayers, fcId, tagLimit,
        firstTurn, lastTurn] = sc.load_scorelog()

    if outdir != "":
        fcId = outdir
    print(fcTags.keys())
    make_directory(fcId)
    write_csv(fcTags, fcData, fcPlayers, fcId, tagLimit, firstTurn, lastTurn)


if __name__ == '__main__':
    parser = ArgumentParser(description='Freeciv Scorelog 2 csv')
    parser.add_argument('filename', nargs='?', default='freeciv-score.log',
                        help='freeciv scorelog filename (default: %(default)s)')
    parser.add_argument('-dir', type=str, metavar='output_direcotry', nargs='?', default="",
                        help='Output directory for csv (default: id given in freeciv-score.log')
    args = parser.parse_args()
    main(args.filename, args.dir)
