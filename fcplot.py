import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties
from argparse import ArgumentParser


def read_file(filename):
    return pd.read_csv(filename, index_col='turn')

def limit_to_players(csv, plist):
    return csv.reindex(plist)
    
def main(filename, plottype, playerlist, excludelist, xlim, ylim, yname):
    
    data = read_file(filename)

    #remove unnamed
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

    #fill Nan as 0
    data.fillna(0, inplace=True)
    
    #array kicked
    dt = data.T

    
    if playerlist != "all":
        player_list = playerlist.split(':')
        print("Included players:", player_list)
        
    if excludelist != "none":
        exclude_list = excludelist.split(':')
        print("Excommunicated players:", exclude_list)
    
    if ylim != "nolimits":
        y = ylim.split(':')
        ymin = y[0]
        ymax = y[1]
        print(f"Y axis min set to {ymin}, max to {ymax}")
        
    if xlim != "nolimits":
        x = xlim.split(':')
        xmin = x[0]
        xmax = x[1]
        print(f"X axis min set to {ymin}, max to {ymax}")
        
    if yname != "":
        filename = yname
     
    if plottype == 'percentage':
        #rows = dt.reindex(["louis94","aaa","bbb","ccc"])
        if playerlist != "all":
            dt = limit_to_players(dt, player_list)
            
        if excludelist != "none":
            dt = dt.drop(exclude_list)
        rows = dt
        rows = (100. * rows / rows.sum()).round(2)
        z = rows.T.plot.area(xlabel="turn", ylabel=filename)
        
        if ylim != "nolimits":
            z.set_ylim(ymin, ymax)
            
        if xlim != "nolimits":
            z.set_xlim(xmin, xmax)
        #z.set_ylim(-100, 100)
        plt.legend(loc='upper left')
        plt.show()
            
    if plottype == 'simple':
        if playerlist != "all":
            data = data[player_list]
        
        if excludelist != "none":
            for i in exclude_list:
                data = data.loc[:, ~data.columns.str.contains(i)]

        z = data.plot(xlabel="turn", ylabel=filename)
        #z = data.plot()
        if ylim != "nolimits":
            z.set_ylim(ymin, ymax)
        if xlim != "nolimits":
            z.set_xlim(xmin, xmax)
        plt.show()
    #jakiś błąd z landarea
    
    #plt.style.use('ggplot')
    #data.plot(kind='bar')

    #rows = dt.reindex(["louis94","aaa","bbb","ccc"])
    #print(rows)
    #rows.T.plot(kind='bar',xlabel="turn", ylabel="score")
    #rows.T.plot.hexbin(xlabel="turn", ylabel="score")
    #data.plot()
    #df.plot(xlabel="new x", ylabel="new y")
    

if __name__ == '__main__':
    parser = ArgumentParser(description='Plot csv files')
    parser.add_argument('filename',nargs='?', default='',
                         help='csv file to read (default: %(default)s)')
    parser.add_argument('-type', type=str, metavar='plot type',nargs='?', default="simple",
                          help='supported types: simple(default), percentage')
    parser.add_argument('-playerlist', type=str, metavar='players only',nargs='?', default="all",
                          help='include only given players - seperated by colon, eg aa:bb:cc (default: %(default)s)')
    parser.add_argument('-excludelist', type=str, metavar='exclude players',nargs='?', default="none",
                          help='exclude given players - seperated by colon, eg aa:bb:cc (default: %(default)s)')
    parser.add_argument('-xlim', type=str, metavar='xlim',nargs='?', default="nolimits",
                          help='min:max of x axis eg 0:100 (default: %(default)s)')
    parser.add_argument('-ylim', type=str, metavar='ylim',nargs='?', default="nolimits",
                          help='min:max of y axis eg 0:100 (default: %(default)s)')
    parser.add_argument('-yname', type=str, metavar='ylegend',nargs='?', default="",
                          help='name of Y axis (default: filename')
    args = parser.parse_args()
    main(args.filename, args.type, args.playerlist, args.excludelist, args.xlim, args.ylim, args.yname)
    
    