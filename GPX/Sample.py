# encoding utf8

# ----------------------------------------------------------------

# stdlib
import xml.dom.minidom

# others

# mines
from smlutils import childElements, radian2degree

# ----------------------------------------------------------------

PAUSE = 10
LAP = 20
POINT = 30

class Sample:
    def __init__(self, xml):
        """
            xml est un xml.dom.Node
            le Sample peut être de 3 types :
                - pause : heure et durée de la pause
                - lap : heure, durée et distance (energy?)
                - position : lat et lon, altitude en option
        """
        self.xml = xml
        self.type = None # PAUSE, LAP ou POINT
        
        self.time = None
        self.utc = None # pour le GPX et le 1er point
        
        self.statut = False
        
        self.dist = None # pour les laps
        self.duree = None # pour les laps et pauses
        
        self.lat = None
        self.lon = None
        self.alt = None
        
        self.parse_xml()
    
    
    def parse_xml(self):
    # pour simplifier je reprends l'approche de ambit2xml :
        for node in childElements(self.xml):
            key = node.tagName.lower()
            if key == "time":   # systématique ?
                self.time = float(node.firstChild.nodeValue)
            elif key == "utc":    # systématique ?
                self.utc = node.firstChild.nodeValue
                
            elif key == "latitude":
                self.lat = radian2degree(float(node.firstChild.nodeValue))
                self.type = POINT
            elif key == "longitude":
                self.lon = radian2degree(float(node.firstChild.nodeValue))
                self.type = POINT
            elif key == "altitude":
                self.alt = float(node.firstChild.nodeValue)
                # self.type = POINT
            elif key == "gpsaltitude":
                self.alt = float(node.firstChild.nodeValue)
                # self.type = POINT

            # elif key == "hr":
                # hr = int((float(node.firstChild.nodeValue))*60+0.5) # Rounding
            # elif key == "temperature":
                # temperature = float(node.firstChild.nodeValue)-273 # K -> °C
            elif key == "distance":
                self.dist = float(node.firstChild.nodeValue)
            elif key == "duration":
                self.duree = float(node.firstChild.nodeValue)

            elif key == "events":
                for subsam in childElements(node):
                    if subsam.tagName.lower() == "pause":
                        self.type = PAUSE
                    elif subsam.tagName.lower() == "lap":
                        self.type = LAP
                    for subevent in childElements(subsam):
                        evtkey = subevent.tagName.lower()
                        if evtkey == "distance":
                            self.dist = float(subevent.firstChild.nodeValue)    # depuis la dernière pause
                        elif evtkey == "duration":
                            self.duree = float(subevent.firstChild.nodeValue)   # depuis la dernière pause
                            # comportement bizarre : pour l'arrêt de la pause, seule la 1ère a une durée
                            # au final je pense que cette info ne sert à rien
                        elif evtkey == "state":
                            self.statut = eval(subevent.firstChild.nodeValue)

    def __str__(self):
        retour = "%.1f" % self.time
        if self.type == PAUSE:
            retour += " PAUSE %s" % ("ON" if self.statut else "OFF")#, self.dist, self.duree)
        elif self.type == LAP:
            retour += " LAP (%.1f m %.1f s)" % (self.dist, self.duree)
        elif self.type == POINT:
            if self.lat and self.lon:
                retour += " pos(%.6f, %.6f)" % (self.lat, self.lon)
            if self.alt:
                retour += " alt(%d)" % self.alt
            if self.dist:
                retour += " dist(%d)" % self.dist
            if self.duree:
                retour += " duree(%d)" % self.duree
        return retour
        
