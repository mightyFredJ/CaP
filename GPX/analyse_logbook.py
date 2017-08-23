# encoding utf8

# ----------------------------------------------------------------

# stdlib
import argparse
from pathlib import Path
import copy
import re
from collections import defaultdict
from pprint import pformat

from xml.dom.minidom import parse as parse_xml, getDOMImplementation
from xml.dom import Node

# others

# mines
from smlutils import almost_in, strUTC2date, sec_2_chrono, get_attributes

#%% ---------------------------------------
# définition des arguments possibles

argparser = argparse.ArgumentParser(description="""Manipulation de logbook""")

group = argparser.add_argument_group("fichiers")
group.add_argument("-i", "--input", type=str, help="input file", default='C:\\Users\\fj221066\\Documents\\xPerso\\Historique de FredJ.logbook')
group.add_argument("-o", "--output", help="file to produce", type=str, default=None)   # pas d'output = sortie console seult

group = argparser.add_argument_group("options")
group.add_argument("-a", "--analyze", help="analyze content", action='store_true', default=True)
group.add_argument(      "--elt", help="elements to analyze (regexes)", action='append', default=[])
group.add_argument(      "--att", help="print attribute", action='append', default=[])
group.add_argument("-s", "--split", help="split year-by-year", action='store_true', default=False)

group = argparser.add_argument_group("debug")
group.add_argument("-v", "--verbose",   help="mode verbeux",    action='store_true',    default=True)
group.add_argument("-q", "--quiet",     help="mode taiseux",    action='store_true',    default=False)
group.add_argument("-d", "--debug",     help="mode debug",      action='store_true',    default=False)

args = argparser.parse_args()

if len(args.elt) == 0:
    args.elt.append('.*')

#%% ---------------------------------------
   
class Activity:
    """
        <Activity referenceId="ec7eed82-8824-4f17-be41-56c68d649157" startTime="2010-01-13T19:41:02Z" hasStartTime="true" totalTime="3807.0499999999997" totalDistance="10739.75" totalAscend="143.33" totalDescend="-144.3" averageHeartRate="146.29" maximumHeartRate="185.94" totalCalories="778" categoryId="fa756214-cf71-11db-9705-005056c00008" categoryName="Mes activités" location="St Rémy / Beauplan" useEnteredData="false">
          <Metadata created="2010-01-14T21:56:38Z" modified="2010-05-23T10:45:15Z" source="importé de Garmin - Forerunner 305 " />
          <Laps>
            <Lap startTime="2010-01-13T19:41:02Z" totalTime="3807.0499999999997" totalCalories="778" />
          </Laps>
          <Weather conditions="Clouds" conditionsText="sol mouillé" />
          <GPSRoute>
            <TrackData version="2"><![CDATA[ToSvJQA...4lkI=]]></TrackData>
          </GPSRoute>
          <HeartRateTrack>
            <TrackData version="1"><![CDATA[AU6EryUAA...AtuEItwEIk=]]></TrackData>
          </HeartRateTrack>
          <TimerPauses>
            <Pause start="2010-01-13T20:01:45Z" duration="121" />
            <Pause start="2010-01-13T20:16:06Z" duration="15" />
            <Pause start="2010-01-13T20:36:00Z" duration="265" />
          </TimerPauses>
          <ExtensionData>
            <Plugins>
              <Plugin id="264fbd17-8a81-4cfa-b739-77c70bcefb53" text="SRTM3_N48E002"><![CDATA[AZsDAAAf...G+qFQAA]]></Plugin>
            </Plugins>
          </ExtensionData>
        </Activity>
    """
    
    def __init__(self, xml):
        self.xml = xml
        self.date = strUTC2date(xml.getAttribute('startTime'))
        self.time = xml.getAttribute('totalTime')
        if self.time: self.time = float(self.time)
        self.dist = xml.getAttribute('totalDistance')
        if self.dist:
            self.dist = float(self.dist)
        else:
            self.dist = 0
        self.hasTrack = len(xml.getElementsByTagName('GPSRoute')) > 0
        self.hasHeart = len(xml.getElementsByTagName('HeartRateTrack')) > 0
    
    def __str__(self):
        retour = "Activité du {dat} : {dist:.1f} km en {dur}".format(
                dat=self.date.strftime('%d/%m/%Y %H:%M:%S'), dur=sec_2_chrono(self.time), dist=self.dist/1000.
            )
        return retour

#%% ---------------------------------------
# gather data

xmldoc = parse_xml(args.input)
rootelt = xmldoc.childNodes[0]

activities = defaultdict(list)  # { year: [activities] }
equipment = []

# scan content
for child in rootelt.childNodes:
    if child.nodeType != Node.ELEMENT_NODE:
        continue
    
    if args.analyze and almost_in(child.tagName, args.elt):
        print(child.tagName)
        print('    %d children' % child.childNodes.length)

        atts = get_attributes(child, args.att)
        if atts:
            print('\n'.join(['    %s' % a for a in atts]))

        for subchild in child.childNodes:
            if subchild.nodeType != Node.ELEMENT_NODE:
                continue
            atts = get_attributes(subchild, args.att)
            if atts:
                print('\n'.join(['        %s' % a for a in atts]))
            

    if child.tagName == 'Activities':
        for subchild in child.childNodes:
            if subchild.nodeType == Node.ELEMENT_NODE:
                act = Activity(subchild)
                if act.date.year == 1:
                    print(subchild.toxml())
                activities[act.date.year].append(act)

    if child.tagName == 'Equipment':
        for subchild in child.childNodes:
            if subchild.nodeType == Node.ELEMENT_NODE:
                equipment.append('<EquipmentItem Id="{id}" '
                                 'Name="{brand} - {model}" />'.format(
                                    id=subchild.getAttribute('referenceId'),
                                    brand=subchild.getAttribute('brand'),
                                    model=subchild.getAttribute('model'),
                                    )
                                )

#%% ---------------------------------------
# print some infos

print()
if args.analyze:
    print("%d activités collectées" % sum([len(acts) for year, acts in activities.items()]))
    print("\n".join(["%d : %d" % (year, len(acts)) for year, acts in sorted(activities.items())]))
    
    print()
    print("%d matériels collectés" % len(equipment))
    print(pformat(equipment, width=100))

print()

#%% ---------------------------------------
# manips


if args.split:
    print('split')
    
    for year, acts in activities.items():
        # get a copy of the full xml
        newdoc = copy.copy(xmldoc)
        newroot = newdoc.childNodes[0]

        # create a <Activities> elt for this year
        newActivites = newdoc.createElement('Activities')
        for act in acts:
            newActivites.appendChild(act.xml)

        # replace the old full <Activities>
        oldActivities = newroot.getElementsByTagName('Activities')[0]
        newroot.appendChild(newActivites)
        newroot.replaceChild(newActivites, oldActivities)
        
        # save it as xml
        newxmlfile = re.sub('(?=\.logbook)', '-%d'%year, Path(args.input).name)
        print('    saving', newxmlfile)
        with open(newxmlfile, 'w') as fxml:
            # newdoc.writexml(fxml) marche pas : pb d'encoding (sauvé en ascii)
            fxml.write(newdoc.toxml(encoding='utf-8').decode('latin-1'))
