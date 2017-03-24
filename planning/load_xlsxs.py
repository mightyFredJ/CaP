# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:13:52 2015

Lecture des fichiers xlsx PRIS
    pour chaque type de fichier on renvoit un DataFrame

@author: fj221066
"""

import pandas as pd
import logging
import datetime

# ----------------------------------------------------------------

# utilisation d'alias pour les clés (noms de colonnes)
kDate = 'Date'
kDist = 'Distance (km)'
kAsc  = 'Ascendant (m)'
kTime = 'Durée (h)'
kNom  = 'Nom'               # courses uniquement
kDiff = 'Difficulté (ekm)'  # pas dans le rapport

kPace = 'Allure moy. (min/km)'
kVit  = 'Vitesse moy. (km/h)'

# ----------------------------------------------------------------

def load_data(xls_filename = './ReactorStatusReport2.xlsx',
              wanted_sheet = 0,
              parse_cols = "A:D", # défaut pour toutes les courses
            **kwargs):
    xlPRIS = pd.ExcelFile(xls_filename)

    print('    %d feuilles :' % len(xlPRIS.sheet_names))
    for sheet_name in xlPRIS.sheet_names:
        print('        %s' % sheet_name)

    data_sheet = xlPRIS.parse(wanted_sheet,
                              index_col='Date',
                              parse_cols=parse_cols)
    # au cas où
    if kVit in data_sheet.columns:
        data_sheet.drop(kVit, axis=1, inplace=1)
    if kPace in data_sheet.columns:
        data_sheet.drop(kPace, axis=1, inplace=1)

    print("\n%d colonnes :" % (len(data_sheet.columns)))
    # print(data_sheet.dtypes)
    for c in data_sheet.columns:
        print('    %s : %s' % (c, type(data_sheet.iloc[0][c])))
    print('index :', type(data_sheet.index))
    print("\n", data_sheet.head())

    return data_sheet

# ----------------------------------------------------------------

def manip_xlsx_data(data):
    """ qqs opérations sur les données brutes chargées d'un rapport
        data est un pd.DataFrame
    """

    # hack : on convertit en float les strings avec des espaces (milliers)
    #   ex. "4 450" -> 4450.
    import re
    data[kAsc] = [ float(re.sub(r'\s+', '', str(a))) for a in data[kAsc] ]

    # hack : on vérifie que les durées sont en datetime.time et non float
    if type(data.iloc[0][kTime]) == str:
        data[kTime] = [ datetime.datetime.strptime(t, "%H:%M:%S") for t in data[kTime] ]

    # hack : on convertit les durées (datetime.time) en Timedelta...
    data[kTime] = [ pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second) for t in data[kTime] ]
    #   ... puis en heures
    data[kTime] = [ float(t.total_seconds())/3600 for t in data[kTime] ]

    # ajout colonne perso
    data[kDiff] = data[kDist] + data[kAsc] / 100.

    return data

# ----------------------------------------------------------------

def merge_on_name(data):
    " fusion des activités qui ont le même nom "

    # opération groupby : renvoie un objet GroupBy
    gb = data.groupby([kNom])
    # la prop groups contient pour chq nom la liste des index,
    #   on garde la 1ère date de chaque nom dans un nveau dict
    first_dates = dict()
    for key, val in gb.groups.items():
        first_dates[key] = val[0]
    first_dates = {
        kNom: list(first_dates.keys()),
        kDate: list(first_dates.values())
        }

    # on transforme le groupby en DataFrame,
    #   l'index est le nom, il n'y a plus de date ici
    df = gb.agg({kDist: sum, kAsc: sum, kTime: sum, kDiff: sum})

    # on transforme les index de dates en DataFrame
    dfdates = pd.DataFrame(first_dates) # par défaut l'index est [0, 1, ...]
    dfdates = dfdates.set_index(kNom)

    # on rajoute ces dates dans le DataFrame groupé
    df = df.join(dfdates)

    # pour l'instant les noms sont dans l'index et les dates dans 1 colonne,
    # pour inverser les 2, on :
    #   1- copie les noms sous forme d'une nouvelle colonne
    df[kNom] = df.index
    #   2- assigne la colonne date à l'index (cette colonne disparait alors)
    df = df.set_index(kDate)

    return df

# ----------------------------------------------------------------

if __name__ == "__main__":
    'tests'

    print('\n---- loading data ----\n')
    xlsxfile = "Dev\\CaP\\perso\\rapport2015.xlsx"
    data = load_data("C:\\Users\\fj221066\\Documents\\" + xlsxfile,
          wanted_sheet='courses', parse_cols="A:D;G")

    print('\n---- exploring raw data ----\n')
    print(data[ data[kNom]=='WEC'] )

    print('\n---- normalizing data BEFORE merging ----\n')
    data = manip_xlsx_data(data)
    print(data[ data[kNom]=='WEC'] )

    print('\n---- searching data AFTER merging ----\n')
    data = merge_on_name(data)
    print(data[ data[kNom]=='WEC'] )
