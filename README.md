# README
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

## Freeciv scorelog2csv
 Freeciv Scorelog to csv format - converts freeciv scorelog to csv format.
 Requires python3
###
Example:
Load default freeciv-score.log and create dir x and convert csv there.
*python.exe freeciv-score-log-2csv.py -dir x*

Load file score.log and create dir zdir and convert csv there.
*python.exe freeciv-score-log-2csv.py score.log -dir zdir*


## Freeciv fcplot
 Fcplot - plots score from given .csv files. Requires python *pandas* and *matplotlib*

Examples:
*python.exe fcplot.py .\x\score.csv -ylim 0:2000*

Default simple plot with with limited y axis to 2000
![Screenshot](https://user-images.githubusercontent.com/43116166/94064106-71ff8580-fde9-11ea-801e-cc819fffc372.png)

*python.exe fcplot.py .\x\mfg.csv -starchange .\x\gov.csv*

Shows production and marks government changes with stars
![Screenshot](https://user-images.githubusercontent.com/43116166/94064107-71ff8580-fde9-11ea-9dc4-60b95ec53a55.png)

*python.exe' fcplot.py .\x\bnp.csv -type percentage*

Shows economy as percentage per turn
![Screenshot](https://user-images.githubusercontent.com/43116166/94064108-72981c00-fde9-11ea-886b-066d559f47da.png)

*python.exe fcplot.py .\x\unitskilled.csv -type heatmap -chg_inc -xlim 50:90*

Shows unit kill heatmap between turns 50-90, uses chg_inc switch to change how unitskilled.csv is organized
![Screenshot](https://user-images.githubusercontent.com/43116166/94064103-70ce5880-fde9-11ea-86ca-9c4f869824f0.png)

*python.exe' fcplot.py .\x\score.csv -top 5*

Shows score for best 5 players

To see more options use *python.exe' fcplot.py --help*


 **Enjoy!**