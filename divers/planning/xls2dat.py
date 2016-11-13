# encoding UTF8
"""
    pt utilitaire de conversion du format Excel en équivalent SportTracks
"""

# stdlib
import argparse
import datetime
from collections import OrderedDict, defaultdict

# other libs
import pandas as pd

# ----------------------------------------------------------------

parser = argparse.ArgumentParser(description=u'conversion format planning')

grp = parser.add_argument_group('targets')
grp.add_argument("-x", "--xlsx", dest='xlsx_filename', type=str, help='xlsx file to open', required=True)
grp.add_argument("-s", "--sheet", dest='sheet_name', type=str, help='sheet to load', required=True)

grp = parser.add_argument_group('options')
grp.add_argument("-r", "--skiprows", type=int, default=0, help="rows to skip (before days' line)")
grp.add_argument("-o", "--output", type=str, default=None, help="output file")
grp.add_argument(      "--maxit", type=int, default=100, help="Nb max iterations")

user_args = parser.parse_args()

# ----------------------------------------------------------------
# chargement données d'entrée

colonnes = []
for i in range(5): # lun .. ven
    colonnes.append(pd.Timedelta('%d days %d hours' % (i, 5))) # matin
    colonnes.append(pd.Timedelta('%d days %d hours' % (i, 12))) # midi
    colonnes.append(pd.Timedelta('%d days %d hours' % (i, 18))) # soir
colonnes.append(pd.Timedelta('%d days %d hours' % (5, 10))) # sam
colonnes.append(pd.Timedelta('%d days %d hours' % (6, 10))) # dim

xlInput = pd.ExcelFile(user_args.xlsx_filename)
data = xlInput.parse(user_args.sheet_name,
                     skiprows=user_args.skiprows + 1,   # +1 : on saute par-dessus les jours (inutiles)
                     index_col=0,
                     parse_cols='B,D:T',
                     # na_values=['x', 'X'],
                    )

# gestion manuelle des valeurs pourries, c'est + simple au final
data.replace(r'.*[a-zA-Z]+.*', '', inplace=True, regex=True)
data.replace('', 0, inplace=True)
data.fillna('0', inplace=True)
print(type(data.index[0]), data.index[0])
print(data.head())
# raise(RuntimeError(pd.__version__))

# ----------------------------------------------------------------
# traitement ligne à ligne

for week in data.index[:5]:
    # print(week, end=': ')
    print('week', week)
    for isubday, subday in enumerate(data.loc[week]):
        # print(subday, end=', ')
        if float(subday) > 0:
            print(week + colonnes[isubday],
                    subday)
    print()

# ----------------------------------------------------------------
# création new DataFrame

cols = "Date;Distance (km);Ascendant (m);Durée (h);Allure moy. (min/km);Vitesse moy. (km/h);Nom;auto".split(";")
rows = OrderedDict()
for c in cols:
    rows[c] = []
# idx = []
mapAsc = {12: 0, 18: 200, 24:400}
def mktime(h, m, s):
    return "%02d:%02d:%02d"%(h, m, s)
    # return datetime.datetime.strptime("%02d:%02d:%02d"%(h, m, s), "%H:%M:%S") pb dans l'enregistrement xlsx
mapTim = {
    12: mktime(1, 0, 0),
    18: mktime(1, 50, 0),
    24: mktime(2, 50, 0)
    }

for week in data.index:
    for isubday, subday in enumerate(data.loc[week]):
        if float(subday) > 0:
            date = week + colonnes[isubday] #idx.append()
            dist = subday
            roundeddist = dist
            
            # cas spéciaux
            if dist == 21.12:
                asc, tim = 550, mktime(3, 15, 0)
            elif dist == 69:
                asc, tim = 2200, mktime(10, 0, 0)
            elif dist == 95:
                asc, tim = 5200, mktime(20, 0, 0)
            elif dist == 7.2:
                asc, tim = 400, mktime(0, 55, 0)
            # cas 'normaux'
            elif dist <= 9.9:
                asc, tim =   0, mktime(0, 30, 0)
            elif dist <= 13.9:
                asc, tim =   0, mktime(1,  0, 0)
            elif dist <= 18.1:
                asc, tim =   0, mktime(1, 30, 0)
            elif dist <= 18.4:
                asc, tim = 200, mktime(2,  0, 0)
            elif dist <= 22.9:
                asc, tim = 400, mktime(2,  0, 0)
            elif dist <= 24.9:
                asc, tim = 400, mktime(2, 50, 0)
            else:
                asc, tim = 400, mktime(3,  0, 0)
                
            #                               pace, speed, nom, auto
            vals = [date, subday, asc, tim, 0, 0, '', 1]
            for icol, col in enumerate(rows.keys()):
                rows[col].append(vals[icol])
# print(rows)
planning = pd.DataFrame(rows)
# print(planning.dtypes)
print(planning.head(10))
print(type(planning.iloc[0]['Durée (h)']), planning.iloc[0]['Durée (h)'])

planning.to_excel(excel_writer='planning.xlsx', sheet_name='planning', index=False)
# planning.to_csv('planning.csv')

# TODO :
# charger les données du fichier planning.xlsx dans DataFrame existing
# fusionner avec data : 