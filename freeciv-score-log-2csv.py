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
from argparse import ArgumentParser

def run_forest(filename):
    line_number = 0

    FCid = ""
    FCtags = {}
    FCturns = {}
    FCplayers = {}
    FCdata = {}
    taglimit  = []

    firstturn = 0

    with open(filename, "r") as reader:
        all = reader.readlines()
        
        while True:
            
            if (len(all)) == 0:
                break
            line = all.pop(0)
            line_number += 1
            if line[0] in ['\n', "#"]:
                continue
        
            line = line.strip()
            command, args = str.split(line, maxsplit = 1)

            if command == "id":
                FCid = args
                
            elif command == "tag":
                tid, descr = str.split(args, maxsplit = 1)
                tid = int(tid)
                FCtags[tid] = descr

            elif command == "turn":
                turn, num, descr = str.split(args, maxsplit = 2)
                turn = int(turn)
                num = int(num)
                FCturns[turn] = (num, descr)

            elif command == "addplayer":
                turn, pid, name = str.split(args, maxsplit = 2)
                turn = int(turn)
                pid = int(pid)
                if pid in FCplayers:
                    FCplayers[pid][1].append((turn,None))
                else:
                    FCplayers[pid] = (name, [(turn, None)])
                print(name);

            elif command == "delplayer":
                turn, pid = str.split(args, maxsplit = 1)
                turn = int(turn)
                pid = int(pid)
                if pid in FCplayers:
                    begturn = FCplayers[pid][1][-1][0]
                    FCplayers[pid][1][-1] = (begturn, turn)
                else:
                    print ("Can't delete nonexisting player.")

            elif command == "data":
                turn, tid, pid, value = str.split(args, maxsplit = 3)
                turn = int(turn)
                tid = int(tid)
                pid = int(pid)
                value = float(value)

                if tid not in FCdata:
                    FCdata[tid] = {}
                if turn not in FCdata[tid]:
                    FCdata[tid][turn] = {}
                FCdata[tid][turn][pid] = value

    lastturn = line_number
    
    for tid in FCtags.keys():

        if not (len(taglimit) == 0 or FCtags[tid] in taglimit):
            continue

        filename = FCtags[tid] + ".csv"
        
        if not os.path.exists(FCid):
            os.makedirs(FCid)
            
        with open(FCid +'/' + filename, 'w') as out:

            # Header
            out.write("\"turn\",")
            for pid in FCplayers.keys():
                out.write("\"%s\"," % FCplayers[pid][0])
            out.write("\n")

            # Data
            for turn in range(firstturn, lastturn):
                if turn in FCdata[tid]:
                    out.write("%d," % turn)
                    for pid in FCplayers.keys():
                        if pid in FCdata[tid][turn]:
                            out.write("%d," % FCdata[tid][turn][pid])
                        else:
                            out.write(",")
                    out.write("\n")

            out.close()
            print(f"{filename } done")


if __name__ == '__main__':
    parser = ArgumentParser(description='Freeciv Scorelog 2 csv')
    parser.add_argument('filename',nargs='?', default='freeciv-score.log',
                         help='freeciv scorelog filename (default: %(default)s)')
    args = parser.parse_args()
    run_forest(args.filename)
