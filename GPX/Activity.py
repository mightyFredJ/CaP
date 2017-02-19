# encoding utf8

# ----------------------------------------------------------------

# stdlib
import datetime
import xml.dom.minidom
from math import fabs

# others

# mines
import Sample
from smlutils import newId, getChildEltValue, strUTC2date, str2date, sec_2_chrono
from tools.utils import today

# ----------------------------------------------------------------

class Activity:
    """
        parsing inspiré de ambit2xml.py trouvé sur le net
    """

    def __init__(self, xml_devicelog, file):
        """
            xml_devicelog est l'élément contenu dans le <sml></sml>
        """
        assert isinstance(xml_devicelog, xml.dom.Node)
        assert xml_devicelog.nodeType == xml.dom.Node.ELEMENT_NODE
        assert xml_devicelog.tagName == 'DeviceLog'

        self.xml = xml_devicelog
        self.file = file
        
        self.id = newId()       # 8dc0b52f-8d22-41ce-981a-5f6bcdf77c25
        self.starttime = None   # 2016-07-11T09:58:21Z
        self.source = None      # description de l'origine
        self.cur_date = None    # jour de l'extraction, même format que starttime
        self.duration = 0       # 2425.27
        self.distance = 0       # 7238.11
        self.ascent = 0         # pas utilisé par le fitlog, c'est juste pour moi
        self.cals = 0           # 586
        self.laps = []
        self.pauses = []
        self.track = []         # liste de points
        self.__nb_samples = 0   # donnée brute du sml
        self.__pauses_tot = 0   # secondes cumulées d'arrêt, calcul perso
        self.location = None

        self.parse_xml()

# ----------------

    def parse_xml(self):
        """
            parcourt le xml pour collecter les points, pauses, etc
        """
        self.parse_header()
        self.parse_samples()
        
    def parse_header(self):
        """
            extrait les infos générales de l'entête
        """            
        header = self.xml.getElementsByTagName('Header')[0]
        
        self.duration = float(getChildEltValue(header, 'Duration'))
        self.distance = float(getChildEltValue(header, 'Distance'))
        self.type = getChildEltValue(header, 'Activity')
        self.ascent = float(getChildEltValue(header, 'Ascent'))
        self.cals = float(getChildEltValue(header, 'Energy')) / 4184 # Energy est en J, on veut des kcal

        self.__nb_samples = int(getChildEltValue(header, 'LogItemCount'))
        self.starttime = str2date(getChildEltValue(header, 'DateTime')) # datetime à l'heure locale
        # WARNING ce format n'est pas valide pour le fitlog
        
    def parse_samples(self):
        """
            analyse les points
        """            
        samples = self.xml.getElementsByTagName('Samples')[0].getElementsByTagName('Sample')
        self.en_pause = True
        last_hr, last_alt = None, None
        for i, sample in enumerate(samples):
            pt = Sample.Sample(sample)
            if pt.type == Sample.PAUSE:
                self.pauses.append(pt)
                self.en_pause = pt.statut                    
                # print('*** passage en en_pause', self.en_pause, 'from pt.statut', pt.statut)
            elif pt.type == Sample.LAP:
                self.laps.append(pt)
            elif pt.type == Sample.POINT:
                if self.en_pause:
                    # print('*** point ignoré :')
                    pass
                else:
                    if pt.hr is None:
                        pt.hr = last_hr
                # solution on récupère les alt du baromètre
                # -> ça fluctue plus que celles du GPS
                    # if pt.alt is None:   
                        # pt.alt = last_alt
                    self.track.append(pt)
            else:
                last_hr = pt.hr
                last_alt = pt.alt
                continue
        
        self.guessLocation()
        self.guessEquipment()
        
    
    def head(self):
        return "%-8s le %s (%-9s) : %s  %4.1f km / %6.1f m+" % (self.type, self.starttime, self.location, sec_2_chrono(self.duration), self.distance/1e3, self.ascent)

        
    def __str__(self):
        retour = "Activité %s le %s à %s\n" % (self.id, self.starttime, self.location)
        retour += "  %s  %.1f km / %.1f m+\n" % (sec_2_chrono(self.duration), self.distance/1e3, self.ascent)
        retour += "  %d points (sur %d samples)\n" % (len(self.track), self.__nb_samples)
        # retour += "\n    " + "\n    ".join([str(p) for p in self.track]) + "\n"
        retour += "  %d pauses\n" % len(self.pauses)
        # retour += "\n    " + "\n    ".join([str(p) for p in self.pauses]) + "\n"
        retour += "  %d laps\n" % len(self.laps)
        # retour += "\n    " + "\n    ".join([str(p) for p in self.laps]) + "\n"
        return retour
    
    def getAsFitlogFormat(self):
        # utilisation temporaire d'un UTC pour le starttime
        sav_starttime = self.starttime
        if len(self.track) > 0:
            self.starttime = self.track[0].utc
    
        source = 'généré à partir de {self.file}'.format(self=self)
        cur_date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        laps, markers = self.getLapsInFitlogFormat()
        track = self.getTrackInFitlogFormat()
        pauses = self.getPausesInFitlogFormat()
        duree = sec_2_chrono(self.duration)
        location = ('            <Location Name="%s" />\n' % self.location) if self.location else ''
        
        retour =  """
        <Activity StartTime="{self.starttime}" Id="{self.id}">
            <Metadata Source="{source}" Created="{cur_date}" Modified="{cur_date}" />
            <Duration TotalSeconds="{self.duration}" /> <!-- {duree} -->
            <Distance TotalMeters="{self.distance}" />
            <Calories TotalCal="{self.cals:.0f}" />
{laps}
            <Category Id="fa756214-cf71-11db-9705-005056c00008" Name="Mes activités" />
{location}{track}
{pauses}
{markers}
        </Activity>
        """.format(**locals())

        self.starttime = sav_starttime
        return retour.encode('utf8').decode('latin-1')

        
    def getPausesInFitlogFormat(self):
        """
            <Pause EndTime="2016-07-08T10:38:56Z" StartTime="2016-07-08T10:38:54Z" />
        """
        retour = "            <TrackClock>\n"
        for i in range(1, len(self.pauses)-1, 2):
            tps_pause = strUTC2date(self.pauses[i+1].utc) - strUTC2date(self.pauses[i].utc)
            self.__pauses_tot += tps_pause.total_seconds()
            
            # on part de 1 car la 1ère pause ne sert à rien (début de l'activité)
            # on s'arrête à -1 car la dernière ne sert à rien non plus (fin de l'activité)
            retour += '                <Pause StartTime="%s" EndTime="%s" /> <!-- %s -->\n' % (self.pauses[i].utc, self.pauses[i+1].utc, tps_pause)
        retour += "                <!-- total %s d'arrêt -->\n" % sec_2_chrono(self.__pauses_tot)
        retour += "            </TrackClock>"
        return retour
    
    def getTrackInFitlogFormat(self):
        """
            <Track StartTime="2016-07-08T10:31:29Z">
                <pt tm="0" lat="48.7159538269043" lon="2.12979936599731" ele="152.025756835938" />
            </Track>
        """
        retour = '            <Track StartTime="%s">\n' % self.starttime # TODO : UTC nécessaire ?
        
        last_ele = 0

        # 1er scan pour rechercher la 1ère GPSalt connue, on va l'appliquer aux premiers points
        #   pour ne pas démarrer à zéro
        for pt in self.track:
            if pt.alt:
                last_ele = pt.alt
                break
        
        for pt in self.track:
            if pt.alt:
                last_ele = pt.alt
            str_pt = '                <pt tm="%d" lat="%.6f" lon="%.6f" ele="%d" ' % (pt.time, pt.lat, pt.lon, last_ele)
            if pt.hr is not None:
                str_pt += 'hr="%d" ' % pt.hr
            str_pt += '/>\n'
            retour += str_pt
        retour += "            </Track>"
        return retour
    
    def getLapsInFitlogFormat(self):
        """
            renvoie 2 chaînes : les Laps et les Markers
            TODO : les laps n'intègrent pas les pauses
            
            <Laps>
                <Lap StartTime="2016-07-10T12:55:19Z" DurationSeconds="3920.19">
                    <Calories TotalCal="762" />
                </Lap>
                <Lap StartTime="2016-07-10T14:00:40Z" DurationSeconds="3982.85">
                    <Calories TotalCal="751" />
                </Lap>
            </Laps>
            
            <DistanceMarkers>
                <Marker dist="9605.02" />
            </DistanceMarkers>
        """
        retour1 = '            <Laps>\n'
        retour2 = '            <DistanceMarkers>\n'
        
        last_time = self.starttime
        last_dur = 0
        cumul_laps = 0
        
        for lap in self.laps:
            last_dur = lap.duree
            retour1 += """                <Lap StartTime="%s" DurationSeconds="%.1f">
                    <Calories TotalCal="0" /> <!-- %s -->
                </Lap>
""" % (last_time, last_dur, sec_2_chrono(last_dur))
            last_time = lap.utc
            
            retour2 += '                <Marker dist="%.2f" />\n' % lap.dist
            cumul_laps += last_dur
        
        # un tour de plus : ce qu'il reste
        retour1 += """                <Lap StartTime="%s" DurationSeconds="%.1f">
                    <Calories TotalCal="0" /> <!-- %s -->
                </Lap>
""" % (last_time, self.duration-cumul_laps, sec_2_chrono(self.duration-cumul_laps))
        
        retour1 += '            </Laps>'
        retour2 += '            </DistanceMarkers>'
        
        return retour1, retour2
        
        
    def guessLocation(self):
        """ essaie de trouver où a eu lieu le run """

        if len(self.track) == 0:
            return None
        
        # points de départ et d'arrivée
        startpt = (self.track[0].lat, self.track[0].lon)
        endpt = (self.track[-1].lat, self.track[-1].lon)
        
        # lieux connus et leurs coordonnées
        pois = {
            'SQY':     { 'pos': [48.769149, 2.023145], 'precis': 1e-3 }, # aussi 48.769135, 2.023387
            'CEA':     { 'pos': [48.728244, 2.146407], 'precis': 1e-3 },
            'Etival':  { 'pos': [47.958588, 0.085600], 'precis': 1e-3 },
            'Vercors': { 'pos': [45.147801, 5.547975], 'precis': 1e-1 },
            'Gif':     { 'pos': [48.689058, 2.115900], 'precis': 1e-2 },
            'Chevreuse':{ 'pos': [48.708024, 2.032483], 'precis': 1e-3 },
        }
        
        # comparaison des points et des lieux
        startloc = None
        endloc = None        
        for poi, defpoi in pois.items():
            lat, lon = defpoi['pos']
            precis = defpoi['precis']
            if fabs(startpt[0] - lat) < precis and fabs(startpt[1] - lon) < precis:
                startloc = poi
            if fabs(endpt[0] - lat) < precis and fabs(endpt[1] - lon) < precis:
                endloc = poi
        
        # on en déduit le nom final
        if startloc == endloc:
            self.location = startloc
        else:
            self.location = "%s->%s" % (startloc, endloc)
        return self.location
    
    def guessEquipment(self):
        """
            devine de self.location et l'heure de départ quel matériel peut avoir été utilisé
        """
        pass
        