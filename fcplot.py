#python3.6+

# plots data from given .csv files
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

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from argparse import ArgumentParser

#color dict
cold = {
    0 : 'w',
    1 : 'r',
    2 : 'g',
    3 : 'k',
    4 : 'c',
	5 : 'm',
	6 : 'y',
    7 :	'#0088ff',
    8 : 'b',
    9 : '#ff8800',
    10: '#B22222',
    11: '#CD5C5C',
    12: '#FF6347',
    13: '#FFE4B5',
    14: '#BDB76B',
    15: '#228B22',
    16: '#006400',
    17: '#808000',
    18: '#7FFFD4',
    19: '#008B8B',
    20: '#4682B4',
    21: '#00008B',
    22: '#DDA0DD',
    23: '#8B008B',
    24: '#4B0082',
    25: '#F5F5DC',
    26: '#708090',
    27: '#2F4F4F',
    28: '#DEB887',
    29: '#800000',
    30: '#A0522D',
    31: '#FFE4C4'
}

def read_file(filename):
    return pd.read_csv(filename, index_col='turn')

def limit_to_players(csv, plist):
    return csv.reindex(plist)

def plot_simple(data, ylabel, ymin = 0, ymax = 0, log_x = False, log_y = False, colormap = None):
    z = data.plot(xlabel="turn", ylabel=ylabel, logx=log_x, logy = log_y)
    if ymax:
            z.set_ylim(int(ymin), int(ymax))
    plt.show()

def plot_percentage(data, ylabel, ymin = 0, ymax = 0, log_x = False, log_y = False, colormap = None):
    rows = data.T
    rows = (100. * data.T / data.T.sum()).round(2)
    rows = rows.T

    z = rows.plot.area(xlabel="turn", ylabel=ylabel, logx=log_x, logy = log_y)
    if ymax:
        z.set_ylim(int(ymin), int(ymax))

    plt.legend(loc='upper left')
    plt.show()

def plot_stackedbar(data, ylabel, ymin = 0, ymax = 0, log_x = False, log_y = False, colormap = None):
    z = data.plot.bar(stacked=True, xlabel="turn", ylabel=ylabel, logx=log_x, logy = log_y, width = 1.0)
    if ymax:
        z.set_ylim(int(ymin), int(ymax))
    plt.show()

def plot_heatmap(data, ylabel, ymin = 0, ymax = 0, log_x = False, log_y = False, colormap = None):
    dx = data.T
    plt.imshow(data.T, cmap =colormap)
    plt.colorbar()
    plt.xticks(range(len(data)), data.index)
    plt.yticks(range(len(data.columns)), data.columns)
    plt.show()

def plot_heatmap2(data, ylabel, ymin = 0, ymax = 0, log_x = False, log_y = False, colormap = None):
    dx = data.T
    l = len(data)
    dx1 = data[:l // 2]
    dx2 = data[l // 2:l]

    fig, (ax1, ax2) = plt.subplots(2, 1)
    whatever = ax1.imshow(dx1.T, cmap = colormap)
    cbar = fig.colorbar(whatever, ax = ax1)
    ax1.plot()

    whatever = ax2.imshow(dx2.T, cmap = colormap)
    cbar = fig.colorbar(whatever, ax = ax2)
    ax2.plot()

    ax1.set_yticks(range(len(dx2.columns)))
    ax1.set_yticklabels([dx2.columns[x] for x in range(len(dx2.columns))])
    ax2.set_yticks(range(len(dx2.columns)))
    ax2.set_yticklabels([dx2.columns[x] for x in range(len(dx2.columns))])
    plt.show()

def plot_hellokitty(data, ylabel, ymin = 0, ymax = 0, log_x = False, log_y = False, colormap = None):
    plt.text(0.1,0.5, "Hello", fontsize=100)
    plt.text(0.14,0.1, "Kitty", fontsize=100)
    plt.show()

def plot_pie(data, ylabel, ymin = 0, ymax = 0, log_x = False, log_y = False, colormap = None):
    rows = data.T
    rows = rows[ymin]
    z = rows.plot.pie(ylabel=f"turn {str(ymin)}")
    plt.show()

def chginc(data):
    colormap = 'Reds'
    data_copy = data
    xlen = len(data) # rows
    ylen = len(data.columns) #cols

    for y in range(ylen):
        old = 0
        for x in range(xlen):
            z = data.iloc[x,y]
            if z >= old:
                data_copy.iloc[x, y] = z - old
            old = z
    data = data_copy
    return data

def plot_scatter(data, scatter, ylab, xmin = 0, xmax = 0, ymin = 0, ymax = 0):
    global cold
    data3d = read_file(scatter)
    data3d = data3d.loc[:, ~data3d.columns.str.contains('^Unnamed')]

    if xmax:
        data3d = data3d[int(xmin):int(xmax)]

    xlen = len(data) # rows
    ylen = len(data.columns) #cols

    for y in range(ylen):
        for x in range(xlen):
            z = data3d.iloc[x,y]
            xz = data.iloc[x,y]
            col_nr = z % 31
            plt.plot(xz, z, '*', color=cold.get(col_nr, 'blue'))

    #plt.scatter(data, data3d)
    plt.gca().set(xlabel=ylab, ylabel=scatter)
    plt.show()
    exit(0)

def star_change(data, filename, ylab,  xmin = 0, xmax = 0, ymin = 0, ymax = 0, log_x = False, log_y = False):
    data3d = read_file(filename)
    data.fillna(0, inplace=True)
    data3d.fillna(0, inplace=True)

    if xmax:
        data3d = data3d[int(xmin):int(xmax)]

    dd = data3d.to_numpy()
    ddcopy = dd

    xlen = len(dd) # 144
    ylen = len(dd[0]) #19
    for y in range(ylen):
        old = 0
        for x in range(xlen):
            val = ddcopy[x,y]
            if (val == old):
                dd[x,y] = 0
            # put it at end to show at end of graph
            if (val != 0):
                dd[xlen - 1, y] = val
            old = val

    z = data.plot(xlabel="turn", ylabel=ylab, logx=log_x, logy = log_y)
    if ymax:
        z.set_ylim(int(ymin), int(ymax))

    xlen = len(dd) # 144
    ylen = len(dd[0]) #19
    for y in range(ylen):
        for x in range(xlen):
            if dd[x,y] != 0:
                z = data.iloc[x,y]
                col_nr = dd[x,y] % 31  # 31 is number of all colors
                plt.plot(x, z, '*', color=cold[col_nr])

    plt.show()
    exit(0)

def top_players(topx, data):
    stats = data.describe()

    #convert mean to dict
    cols = stats.loc['mean'].to_dict()

    #sort columns by value
    cols = dict(sorted(cols.items(), key=lambda item: item[1]))

    col_list = list(cols)
    #revert list (was sorted from min)
    col_list = col_list[::-1]

    top_list = []
    i = 0
    for item in col_list:
        i += 1
        top_list.append(item)
        if i >= topx:
            break

    print("Top players:", top_list)
    data = data[top_list]
    stats = data.describe()
    print(stats)
    return data

def main(filename, plottype, playerlist, excludelist, xlim, ylim, log_x, log_y, yname, pie_turn,
          topx, scatter, starchange, chg_inc):

    exclude_list = None
    xmin = None
    xmax = None
    ymin = 0
    ymax = 0
    player_list = None
    sec_data = None

    if not filename:
        print("\033[1mMissing filename. Check --help\033[0m")  #Bold
        exit(0)

    data = read_file(filename)
    colormap = "Blues"

    #remove unnamed
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

    #fill dead players score as last one
    data = data.replace(r'\s+', np.nan, regex=True)
    data = data.fillna(method='ffill')

    #fill remaining Nan as 0
    data.fillna(0, inplace=True)

    if xlim != "nolimits":
        x = xlim.split(':')
        xmin = x[0]
        xmax = x[1]
        print(f"X axis min set to {xmin}, max to {xmax}")

    if playerlist != "all":
        player_list = playerlist.split(':')
        print("Included players:", player_list)

    if excludelist != "none":
        exclude_list = excludelist.split(':')
        print("Excommunicated players:", exclude_list)

    if playerlist != "all":
        data = data[player_list]

    if excludelist != "none":
        for i in exclude_list:
            data = data.loc[:, ~data.columns.str.contains(i)]

    if xlim != "nolimits":
        data = data[int(xmin):int(xmax)]

    if topx > 0:
        data = top_players(topx, data)

    if ylim != "nolimits":
        y = ylim.split(':')
        ymin = y[0]
        ymax = y[1]
        print(f"Y axis min set to {ymin}, max to {ymax}")

    if pie_turn != -1:
        plottype = "pie"
        ymin = pie_turn

    if yname != "":
        filename = yname
    else:
        unused , only_file = os.path.split(filename)
        filename = only_file

    if starchange != "none":
        star_change(data, starchange, filename, xmin, xmax, ymin, ymax, log_x, log_y)

    if chg_inc:
        data = chginc(data)

    if scatter != "none":
        plot_scatter(data, scatter,filename, xmin, xmax, ymin, ymax)

    func_dict = {
        'percentage'    : plot_percentage,
        'simple'        : plot_simple,
        'heatmap'       : plot_heatmap,
        'heatmap2'      : plot_heatmap2,
        'hellokitty'    : plot_hellokitty,
        'stackedbar'    : plot_stackedbar,
        'pie'           : plot_pie,
    }
    func_dict[plottype](data, filename, int(ymin), int(ymax), log_x, log_y, colormap)

if __name__ == '__main__':
    parser = ArgumentParser(description='Plot csv files')
    parser.add_argument('filename',nargs='?', default='', help='csv file to read')
    parser.add_argument('-type', type=str, metavar='plot_type',nargs='?', default="simple",
                          help='supported types: simple(default), percentage, stackedbar, heatmap, heatmap2, scatter')
    parser.add_argument('-playerlist', type=str, metavar='list of players',nargs='?', default="all",
                          help='include only given players - seperated by colon, eg aa:bb:cc (default: %(default)s)')
    parser.add_argument('-excludelist', type=str, metavar='list of excluded players',nargs='?', default="none",
                          help='exclude given players - seperated by colon, eg aa:bb:cc (default: %(default)s)')
    parser.add_argument('-xlim', type=str, metavar='min:max',nargs='?', default="nolimits",
                          help='min:max of x axis eg 0:100 (default: %(default)s)')
    parser.add_argument('-ylim', type=str, metavar='min:max',nargs='?', default="nolimits",
                          help='min:max of y axis eg 0:100 (default: %(default)s)')
    parser.add_argument('-yname', type=str, metavar='ylegend',nargs='?', default="",
                          help='name of Y axis (default: filename)')
    parser.add_argument('-logx', help='sets logarythmic X axis', action="store_true")
    parser.add_argument('-logy', help='sets logarythmic Y axis', action="store_true")
    parser.add_argument('-pie', type=int, metavar='turn number',nargs='?', default="-1",
                          help='Pie chart, it negates other options, takes only turn number')
    parser.add_argument('-top', type=int, metavar='N - number of top players',nargs='?', default="-1",
                          help='Shows plots for best N given players based on pandas mean() value')
    parser.add_argument('-scatter', type=str, metavar='filename',nargs='?', default="none",
                          help='scatter plot, filename of another csv (usually gov.csv)')
    parser.add_argument('-starchange', type=str, metavar='filename',nargs='?', default="none",
                          help='shows star when data on given csv changes(usually gov.csv)')
    parser.add_argument('-chg_inc', help='changes incrementing stats to stat per turn. eg from unit built/killed',
                         action="store_true")
    args = parser.parse_args()
    main(args.filename, args.type, args.playerlist, args.excludelist, args.xlim, args.ylim, args.logx,
         args.logy, args.yname, args.pie, args.top, args.scatter, args.starchange, args.chg_inc)

