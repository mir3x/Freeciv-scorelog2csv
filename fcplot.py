#python3.6+

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

from argparse import ArgumentParser


def read_file(filename):
    return pd.read_csv(filename, index_col='turn')

def limit_to_players(csv, plist):
    return csv.reindex(plist)
    
def main(filename, plottype, playerlist, excludelist, xlim, ylim, log_x, log_y, yname, pie_turn, topx):
    
    data = read_file(filename)

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
        stats = data.describe()
            
        #convert mean to dict
        cols = stats.loc['mean'].to_dict()
        
        #sort columns by value
        cols = {k: v for k, v in sorted(cols.items(), key=lambda item: item[1])}
        
        col_list = []
        #make column list
        for k in cols.keys():
            col_list.append(k)
        
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
                
    if pie_turn != -1:
        plottype = "pie"

    
    if ylim != "nolimits":
        y = ylim.split(':')
        ymin = y[0]
        ymax = y[1]
        print(f"Y axis min set to {ymin}, max to {ymax}")
                
    if yname != "":
        filename = yname
        
     
    #array kicked
    dt = data.T
    
    if plottype == 'percentage':

        rows = dt
        rows = (100. * rows / rows.sum()).round(2)
        rows = rows.T
                    
        z = rows.plot.area(xlabel="turn", ylabel=filename, logx=log_x, logy = log_y)
        
        if ylim != "nolimits":
            z.set_ylim(int(ymin), int(ymax))
            
        plt.legend(loc='upper left')
        plt.show()
            
    if plottype == 'simple':
        
        z = data.plot(xlabel="turn", ylabel=filename, logx=log_x, logy = log_y)
        if ylim != "nolimits":
            z.set_ylim(int(ymin), int(ymax))
        plt.show()

    if plottype == 'stackedbar':
        z = data.plot.bar(stacked=True, xlabel="turn", ylabel=filename, logx=log_x, logy = log_y, width = 1.0)
        if ylim != "nolimits":
            z.set_ylim(int(ymin), int(ymax))
        plt.show()

    if plottype == 'pie':
        rows = dt
        rows = rows[pie_turn]
        z = rows.plot.pie(ylabel=("turn " + str(pie_turn)))
        plt.show()
            
if __name__ == '__main__':
    parser = ArgumentParser(description='Plot csv files')
    parser.add_argument('filename',nargs='?', default='', help='csv file to read')
    parser.add_argument('-type', type=str, metavar='plot_type',nargs='?', default="simple",
                          help='supported types: simple(default), percentage, stackedbar')
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
    args = parser.parse_args()
    main(args.filename, args.type, args.playerlist, args.excludelist, args.xlim, args.ylim, args.logx, args.logy, args.yname, args.pie, args.top)
    
    