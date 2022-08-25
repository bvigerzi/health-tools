# trk -> trkseg -> [trkpt -> extensions (OPTIONAL) -> gpxtpx:TrackPointExtension -> gpxtpx:hr]
from xml.dom.minidom import Element
from defusedxml import minidom
import pandas as pd

def trkpt_has_hr(trkpt: Element):
    return trkpt_parse_hr(trkpt) != None

def trkpt_parse_hr(trkpt: Element):
    extensions = trkpt.getElementsByTagName("extensions")
    if(extensions.length >= 1):
        trkptext = extensions.item(0).getElementsByTagName("gpxtpx:TrackPointExtension")
        if(trkptext.length >= 1):
            trkpthr = trkptext.item(0).getElementsByTagName("gpxtpx:hr")
            if(trkpthr.length >= 1):
                return int(trkpthr.item(0).firstChild.data)
    return None

def trkpt_parse_time(trkpt: Element):
    time = trkpt.getElementsByTagName("time")
    if(time.length >= 1):
        return time.item(0).firstChild.data # TODO: convert to datetime ?

result = minidom.parse("data/20220802_163720.gpx")
trkpts = result.getElementsByTagName("trk").item(0).getElementsByTagName("trkseg").item(0).getElementsByTagName("trkpt")
trkpts_with_ext = list(filter(lambda trkpt: trkpt_has_hr(trkpt), trkpts))

all_hr = dict(map(lambda trkpt: (trkpt_parse_time(trkpt), trkpt_parse_hr(trkpt)), trkpts_with_ext))

series = pd.Series(all_hr)
print(series)
print("HR min:", series.min())
print("HR max:", series.max())
print("HR avg.:", series.mean())
