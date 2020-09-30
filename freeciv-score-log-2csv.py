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
from argparse import ArgumentParser


def load_scorelog(filename):

    firstTurn = 0
    lastTurn = 0
    fcId = ""
    fcTags = {}
    fcTurns = {}
    fcPlayers = {}
    fcData = {}
    tagLimit = []

    try:
        with open(filename, "r") as reader:
            all = reader.readlines()

            while True:

                if not all:
                    break
                line = all.pop(0)

                if line[0] in ['\n', "#"]:
                    continue

                lastTurn += 1
                line = line.strip()
                command, args = str.split(line, maxsplit=1)

                if command == "id":
                    fcId = args

                elif command == "tag":
                    tid, descr = str.split(args, maxsplit=1)
                    tid = int(tid)
                    fcTags[tid] = descr

                elif command == "turn":
                    turn, num, descr = str.split(args, maxsplit=2)
                    turn = int(turn)
                    num = int(num)
                    fcTurns[turn] = (num, descr)

                elif command == "addplayer":
                    turn, pid, name = str.split(args, maxsplit=2)
                    turn = int(turn)
                    pid = int(pid)
                    if pid in fcPlayers:
                        fcPlayers[pid][1].append((turn, None))
                    else:
                        fcPlayers[pid] = (name, [(turn, None)])
                    print("Added player: ", name)

                elif command == "delplayer":
                    turn, pid = str.split(args, maxsplit=1)
                    turn = int(turn)
                    pid = int(pid)
                    if pid in fcPlayers:
                        begTurn = fcPlayers[pid][1][-1][0]
                        fcPlayers[pid][1][-1] = (begTurn, turn)
                    else:
                        print("Can't delete nonexisting player.")

                elif command == "data":
                    turn, tid, pid, value = str.split(args, maxsplit=3)
                    turn = int(turn)
                    tid = int(tid)
                    pid = int(pid)
                    value = float(value)

                    if tid not in fcData:
                        fcData[tid] = {}
                    if turn not in fcData[tid]:
                        fcData[tid][turn] = {}
                    fcData[tid][turn][pid] = value
        reader.close()

    except:
        err = sys.exc_info()[0]
        print(f"Error ***{err}*** when reading file {filename}. Exiting")
        exit(1)

    return fcTags, fcData, fcPlayers, fcId, tagLimit, firstTurn, lastTurn


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

        if not (not taglimit or fcTags[tid] in taglimit):
            continue

        filename = fcTags[tid] + ".csv"
        out = None
        try:
            with open(fcId + '/' + filename, 'w') as out:

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
            print(f"Error ***{err}*** when writing file {filename}")

        finally:
            out.close()


def main(filename, outdir):

    block = []
    [fcTags, fcData, fcPlayers, fcId, tagLimit,
        firstTurn, lastTurn] = load_scorelog(filename)

    if outdir != "":
        fcId = outdir

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
