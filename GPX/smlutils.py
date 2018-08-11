# encoding utf8

# ----------------------------------------------------------------

# stdlib
import sys
import doctest
import datetime
from random import getrandbits
import math
import re
import uuid

# others

# mines

# %% -------------------------------------------------------------------

def strUTC2date(s):#, convertInLocalZone = True):
    """ convertit une UTC en datetime.datetime (avec màj heure d'été) """
    try:
        d = datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        try:
            d = datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')    
        except ValueError:
            d = datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')    
        
    # if convertInLocalZone:
        # d += datetime.timedelta(hours=2)

    return d

def str2date(s):
    """ convertit une UTC en datetime.datetime """
    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')

# ----------------------------------------------------------------

def radian2degree(radian):
    return radian * 180.0 / math.pi

# ----------------------------------------------------------------

def sec_2_chrono(sec):
    """
        sec : nombre ou timedelta
        
        >>> for s in 3712, 75, 17837.9, 72650.1, 0:
        ...     print(s, 'sec =', sec_2_chrono(s))
        3712 sec = 01:01:52
        75 sec = 00:01:15
        17837.9 sec = 04:57:18
        72650.1 sec = 20:10:50
        0 sec = 00:00:00
        
        >>> for td in [datetime.timedelta(seconds=999)]:
        ...     print(td, "=", sec_2_chrono(td))
        0:16:39 = 00:16:39
    """
    if isinstance(sec, datetime.timedelta):
        sec = sec.total_seconds()
    elif isinstance(sec, str):
        try:
            sec = int(sec)
        except ValueError:
            sec = 0
    _s = sec % 60
    _m = ((sec - _s)/60) % 60
    _h = (sec - _s - _m*60)/3600
    return "{_h:02.0f}:{_m:02.0f}:{_s:02.0f}".format(**locals())

# ----------------------------------------------------------------

def newId():
    """
        crée un 'Id' SportTracks (en fait un uuid)
    """
    return str(uuid.uuid4())

# ----------------------------------------------------------------
    
def childElements(parent):   
    elements = []
    for child in parent.childNodes:
        if child.nodeType != child.ELEMENT_NODE:
            continue
        elements.append(child)
    return elements

def getChildEltValue(father, child):
    """
        elt = xml.parse('<Sample>  <Time>1.018</Time>  </Sample>')
        getChildEltValue(elt, 'Time')
        1.018
    """
    try:
        return father.getElementsByTagName(child)[0].firstChild.nodeValue
    except BaseException as ex:
        print('father ', father.tagName, ' child ', child)
        raise ex

def get_attributes(elt, atts):
    retour = []
    for attr in atts:
        if elt.attributes and elt.hasAttributes() and elt.hasAttribute(attr):
            retour.append('%s = %s' % (attr, elt.getAttribute(attr)))
    return retour

# ----------------------------------------------------------------

# for i in range(10):
    # print(newId())

txt_fitlog = """<?xml version="1.0" encoding="utf-8"?>
<FitnessWorkbook xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://www.zonefivesoftware.com/xmlschemas/FitnessLogbook/v2">
  <AthleteLog>
    <Athlete Id="aa5318cc-f1e5-4f53-a7f8-c3cedddc9e99" Name="FredJ" />
{Activities}
  </AthleteLog>
</FitnessWorkbook>"""

# txt_activity = """    <Activity StartTime="$starttime" Id="$id">
      # <Metadata Source="$source" Created="$cur_date" Modified="$cur_date" />
      # <Duration TotalSeconds="$duration" />
      # <Distance TotalMeters="$distance" />
      # <Calories TotalCal="$cals" />
      # <Laps>
# $Laps
      # </Laps>
      # <Category Id="fa756214-cf71-11db-9705-005056c00008" Name="Mes activités" />
      # <Location Name="CEA" />
      # <Track StartTime="$starttime">
# $pts
      # </Track>
# $pauses
    # </Activity>
# """

untracked_fields = """
        <Name>Transbaie</Name>
        <EquipmentUsed>
            <EquipmentItem Id="132de178-8f0a-4746-8f75-0c084e44484c" Name="Kalenji - Kiprun" />
        </EquipmentUsed>
"""

# txt_pauses = """      <TrackClock>
        # <Pause EndTime="2016-07-11T10:19:04Z" StartTime="2016-07-11T10:10:36Z" />
        # <Pause EndTime="2016-07-11T10:39:03Z" StartTime="2016-07-11T10:31:06Z" />
        # <Pause EndTime="2016-07-11T10:42:29Z" StartTime="2016-07-11T10:41:10Z" />
      # </TrackClock>"""

# txt_lap = """        <Lap StartTime="2016-07-11T09:58:22Z" DurationSeconds="2425.27">
          # <Calories TotalCal="586" />
        # </Lap>"""
        
# txt_pt = '        <pt tm="%d" lat="%g" lon="%g" ele="%.1f" hr="%d" />'

# # il y a n-1 markers que de laps
# txt_markers = """   <DistanceMarkers>
    # <Marker dist="946.5001" />
    # <Marker dist="1419.024" />
    # <Marker dist="1887.976" />
    # <Marker dist="2360.806" />
    # <Marker dist="2831.17" />
    # <Marker dist="3312.113" />
    # <Marker dist="3786.261" />
    # <Marker dist="4258.477" />
    # <Marker dist="4736.26" />
    # <Marker dist="5215.426" />
   # </DistanceMarkers>"""

#%% ---------------------------------------
   
def almost_in(candidate, patterns):
    """
        cherche si une chaîne matche au moins 1 élément d'une liste de regex
        >>> almost_in('foo', 'fo+')
        True
        >>> almost_in('baz', ['fo+', 'bar'])
        False
        >>> almost_in('baz', ['fo+', 'ba[rz]'])
        True
    """
    if isinstance(patterns, str):
        patterns = [patterns]
    elif isinstance(patterns, list):
        pass
    else:
        raise TypeError('almost_in signature : (str, list), got (%s, %s)' % (type(candidate), type(patterns)))
        
    for pattern in patterns:
        if re.search(pattern, candidate):
            return True
    return False

# %% -------------------------------------------------------------------

if __name__ == "__main__":
    quiet = len(sys.argv) > 1 and '-q' in sys.argv[1]
    if quiet:
        sys.stdout = io.StringIO()

    # ---- do the tests
    opts = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    (fails, tests) = doctest.testmod(optionflags=opts)
    # ---- done

    sys.stdout = sys.__stdout__  # même si not quiet ça ne coûte rien

    if tests == 0:
        print('no tests in this file')
    elif tests > 0 and fails == 0:  # sinon pas d'affichage c'est pénible
        print('%d tests successfully passed' % tests)
    elif quiet:
        print('%d tests over %d FAILED' % (fails, tests))
