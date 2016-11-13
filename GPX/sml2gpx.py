import os
import xml.dom.minidom
import math
import getopt
import sys

def radian2degree(radian):
    return radian * 180.0 / math.pi

def childElements(parent):   
    elements = []
    for child in parent.childNodes:
        if child.nodeType != child.ELEMENT_NODE:
            continue
        elements.append(child)
    return elements

class AmbitXMLParser(object):
    __root = None
    __outputfile = None
    def __init__(self, xml_node, altibaro, noext, outputfile, lastdistance, first=True):
        assert isinstance(xml_node, xml.dom.Node)
        assert xml_node.nodeType == xml_node.ELEMENT_NODE
        self.__root = xml_node
        self.__outputfile = outputfile
        self.__altibaro = altibaro
        self.__altitude = None
        self.__latitude = None
        self.__longitude = None
        self.__hr = None
        self.__temperature = None
        self.__noext = noext
        self.__lastdistance = lastdistance
        self.__first = first
        self.__nb_samples_parsed = 0
        
    def extension(self, hr, temperature):
        if (self.__noext == True):
            return ""
        
        extensionfound = False
        retour = """
      <extensions> 
        <gpxtpx:TrackPointExtension> 
"""
        
        hrext = ""
        if (hr != None):
            extensionfound = True
            retour += "        <gpxtpx:hr>{hr}</gpxtpx:hr>\n".format(hr=hr)
            
        tmpext = ""
        if (temperature != None):
            extensionfound = True
            retour += "        <gpxtpx:atemp>{temp}</gpxtpx:atemp>".format(temp=temperature)
            
        if not extensionfound:
            return ""
            
        retour += """      </gpxtpx:TrackPointExtension>
</extensions>"""
        return retour

        
    def __parse_sample(self, sample, lastdistance, first):
        llatitude = None
        llongitude = None
        time = None
        distance = None
        hr = None
        altitude = None
        temperature = None

        self.__nb_samples_parsed += 1
        
        # Output some '.' for showing progress of conversion
        if self.__nb_samples_parsed % 100 == 0:
            sys.stdout.write(".")
            if self.__nb_samples_parsed % (80*100) == 0:
                sys.stdout.write("\n")
                
        for node in childElements(sample):
            key = node.tagName
            if key.lower() == "latitude":
                llatitude = radian2degree(float(node.firstChild.nodeValue))
            if key.lower() == "longitude":
                llongitude = radian2degree(float(node.firstChild.nodeValue))
            if key.lower() == "utc":
                time = node.firstChild.nodeValue
            if key.lower() == "hr":
                hr = int((float(node.firstChild.nodeValue))*60+0.5) # Rounding
            if key.lower() == "altitude":
                if self.__noalti:
                    altitude = 0
                elif self.__altibaro:
                    altitude = node.firstChild.nodeValue
            if key.lower() == "temperature":
                # Temperature come in Kelvin unit
                temperature = float(node.firstChild.nodeValue)-273
            if key.lower() == "gpsaltitude":
                if self.__noalti:
                    altitude = 0
                elif not self.__altibaro:
                    altitude = node.firstChild.nodeValue
            if key.lower() == "distance":
                distance = float(node.firstChild.nodeValue)
                
        if self.__noext:
            extension = ""
        else:
            extension = self.extension(hr, temperature)
                
        if latitude != None and longitude != None:
            print("""      <trkpt lat="{latitude}" lon="{longitude}">
        <ele>{altitude}</ele>
        <time>{time}</time>{extension}
      </trkpt>""".format(**locals(), file=self.__outputfile))
      

    def __parse_sml(self, sml, lastdistance, first):
        for node in childElements(sml):
            key = node.tagName
            if key.lower() == "devicelog":
                self.__parse_devicelog(node,lastdistance, first)
                return

    def __parse_devicelog(self, devicelog, lastdistance, first):
        for node in childElements(devicelog):
            key = node.tagName
            if key.lower() == "samples":
                self.__parse_samples(node,lastdistance, first)
    
    def __parse_samples(self, samples, lastdistance, first):
        for node in childElements(samples):
            key = node.tagName
            if key.lower() == "sample":
                self.__parse_sample(node,lastdistance, first)
      
    def execute(self):   
        print('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>', file=self.__outputfile)
        print("""
<gpx 
xmlns="http://www.topografix.com/GPX/1/1"
xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" 
creator="ambit2gpx" version="1.1"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
  <metadata>
    <link href="http://code.google.com/p/ambit2gpx/">
      <text>Ambit2GPX</text>
    </link>
  </metadata>
  <trk>
    <trkseg>  
""", file=self.__outputfile)              
        root = self.__root
        lastdist = self.__lastdistance
        fir = self.__first
        for node in childElements(root):
            key = node.tagName
            if key.lower() == "sml":
                self.__parse_sml(node, lastdist, fir)
                break
                
        print("""
    </trkseg>        
  </trk>
</gpx>
""", file=self.__outputfile)

def usage():
    print("""
ambit2gpx [--altibaro] [--noext] filename
Creates a file filename.gpx in GPX format from filename in Suunto Ambit SML format.
If option --altibaro is given, elevation is retrieved from altibaro information. The default is to retrieve GPS elevation information.
If option --noext is given, extended data (hr, temperature, cadence) will not generated. Useful for instance if size of output file matters.
""")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha", ["help", "altibaro", "noext"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    if len(sys.argv[1:]) == 0:
        usage()
        sys.exit(2)
    output = None
    verbose = False
    altibaro = False
    noext = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-a", "--altibaro"):
            altibaro = True
        elif o in ("--noext"):
            noext = True
        else:
            assert False, "unhandled option"
    # ...
    
    filename = args[0]
    (rootfilename, ext) = os.path.splitext(filename)
    if (ext == ""):
        filename += ".sml"
    if (not os.path.exists(filename)):
        print("File {0} doesn't exist".format(filename), file=sys.stderr)
        sys.exit()
    file = open(filename)
    file.readline() # Skip first line
    filecontents = file.read()
    file.close()
    
    print("Parsing file {0}".format(filename))
    doc = xml.dom.minidom.parseString('<?xml version="1.0" encoding="utf-8"?><top>'+filecontents+'</top>')
    assert doc != None
    top = doc.getElementsByTagName('top')
    assert len(top) == 1    
    print("Done.")
    
    outputfilename = rootfilename+ '.gpx'
    outputfile = open(outputfilename, 'w')
    print("Creating file {0}".format(outputfilename))
    AmbitXMLParser(top[0], altibaro, noext, outputfile, lastdistance=0, first=True).execute()
    outputfile.close()
    print("\nDone.")
        
if __name__ == "__main__":
    main()
