
import argparse
from copy import copy
from datetime import datetime

from xml.dom.minidom import parse as parse_xml, getDOMImplementation
from xml.dom import Node

#%% ---------------------------------------
# définition des arguments possibles

argparser = argparse.ArgumentParser(description="""Manipulation de GPX""")

group = argparser.add_argument_group("fichiers")
group.add_argument("inputs", type=str, nargs='+', help="input files")
group.add_argument("-o", "--output", help="file to produce", type=str, default=None)   # pas d'output = sortie console seult

group = argparser.add_argument_group("options")
group.add_argument("-m", "--merge", help="concat files", action='store_true', default=False)
group.add_argument("-i", "--invert", help="invert files", action='store_true', default=False)

group = argparser.add_argument_group("debug")
group.add_argument("-v", "--verbose",   help="mode verbeux",    action='store_true',    default=True)
group.add_argument("-q", "--quiet",     help="mode taiseux",    action='store_true',    default=False)
group.add_argument("-d", "--debug",     help="mode debug",      action='store_true',    default=False)

args = argparser.parse_args()

#%% ---------------------------------------

# liste des traces (sans autres attributs du gpx)
tracks = [] # <trk> including subelems like <name> and <trkseg>

# chargement
for gpx in args.inputs:
    xmldoc = parse_xml(gpx)
    # print(xmldoc)

    rootelt = xmldoc.childNodes[0]
    # print(rootelt.toxml())
    for child in rootelt.childNodes:
        if child.nodeType != Node.ELEMENT_NODE:
            continue
        # print(child.toxml())
        # print(child.tagName)
        if child.tagName == 'trk':
            tracks.append(child)
            # print('    ', len(child.childNodes), 'pts')

#%% ---------------------------------------
# manips

dom = getDOMImplementation()
doc = dom.createDocument(None, "dummy_tag", None)
timefmt = '%Y-%m-%dT%H:%M:%SZ'
print()


if args.invert:
    raise NotImplementedError('option -i/--invert pas encore opérationnelle')

if args.merge:
    merged_track = copy(tracks.pop(0))
    
    # identification heure du dernier point
    last_point = merged_track.getElementsByTagName('trkpt')[-1]
    hour_last_point = last_point.getElementsByTagName('time')[0].firstChild.data
    print('first track ends at', hour_last_point)
    last_hour_prev_trkseg = datetime.strptime(hour_last_point, timefmt)
    print(last_hour_prev_trkseg)
    
    for track in tracks:
        # mise à jour du nom du parcours fusionné
        trackname = track.getElementsByTagName('name')[0].firstChild.data
        merged_track.getElementsByTagName('name')[0].firstChild.data += ' + ' + trackname
        print('\nappending new track', trackname)
        
        # ajout des segments du nveau track
        start_hour_cur_trkseg = None
        for trkseg in track.getElementsByTagName('trkseg'):
            newseg = doc.createElement('trkseg')
            merged_track.appendChild(newseg)
            for pt in trkseg.getElementsByTagName('trkpt'):
                h = pt.getElementsByTagName('time')[0].firstChild.data
                h = datetime.strptime(h, '%Y-%m-%dT%H:%M:%SZ')
                if start_hour_cur_trkseg == None:
                    start_hour_cur_trkseg = h
                    print('    new track starts at', start_hour_cur_trkseg)
                hour_new_point = last_hour_prev_trkseg + (h - start_hour_cur_trkseg)
                newpt = copy(pt)
                newpt.getElementsByTagName('time')[0].firstChild.data = hour_new_point.strftime(timefmt)
                newseg.appendChild(pt)
            last_hour_prev_trkseg = hour_new_point
            print('    last trkseg ends at', last_hour_prev_trkseg)
            
    print('merged track : %d pts' % len(merged_track.childNodes))

    if args.output:
        with open(args.output, 'w') as fxml:
            fxml.write(merged_track.toprettyxml(newl=""))
    else:
        print(merged_track.toxml())
    
print(""" TODO :
pour l'instant on manipule les trkseg 1 à 1,
en fait il faut les fusionner
""")
