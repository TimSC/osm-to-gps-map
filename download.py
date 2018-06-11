from __future__ import print_function
import math, os, bz2, urlutil, tiles, time, pycurl, gzip, sys
from pyo5m import OsmData
from io import BytesIO

def GetTile(x, y, zoom, outFina):
	
	topLeft = tiles.num2deg(x, y, zoom)
	bottomRight = tiles.num2deg(x+1, y+1, zoom)

	#url = "http://fosm.org/api/0.6/map?bbox={0},{1},{2},{3}".format(topLeft[1],bottomRight[0],bottomRight[1],topLeft[0])
	url = "http://sodium:8010/api/0.6/map?bbox={0},{1},{2},{3}".format(topLeft[1],bottomRight[0],bottomRight[1],topLeft[0])
	print (url)
	timeout = 1
	waiting = 1
	
	while waiting:
		try:
			body, header = urlutil.Get(url)
			responseCode = urlutil.HeaderResponseCode(header)
			print (responseCode)
			if responseCode == "HTTP/1.1 200 OK":
				waiting = 0
			else:
				time.sleep(timeout)
				timeout *= 2

		except pycurl.error:
			time.sleep(timeout)
			timeout *= 2

	extSp = os.path.splitext(outFina)
	extSp2 = os.path.splitext(extSp[0])

	if extSp[1] == ".bz2" and extSp2[1] == ".osm":
		outFi = bz2.BZ2File(outFina,"w")
		outFi.write(body)

	if extSp[1] == ".gz" and extSp2[1] == ".o5m":
		osmData = OsmData.OsmData()
		osmData.LoadFromOsmXml(BytesIO(body))
		osmData.SaveToO5m(gzip.open(outFina, "wb"))

	return 1

if __name__ == "__main__":
	#tileBL = (0, 4095) #Planet
	#tileTR = (4095, 0) #Planet

	#tileBL = tiles.deg2num(51.7882364, -3.4765251, 12) #Hampshire?
	#tileTR = tiles.deg2num(52.3707994, -2.2782056, 12) #Hampshire?

	#tileBL = tiles.deg2num(27.673799, 32.1679688, 12) #Sinai
	#tileTR = tiles.deg2num(31.297328, 35.0024414, 12) #Sinai

	#tileBL = tiles.deg2num(51.00434, -4.02825, 12) #Exmoor
	#tileTR = tiles.deg2num(51.26630, -3.26607, 12) #Exmoor

	#tileBL = tiles.deg2num(49.0018439, -0.6632996, 12) #Caen
	#tileTR = tiles.deg2num(49.3644891, 0.0054932, 12) #Caen

	tileBL = tiles.deg2num(49.6676278, -14.765625, 12) #UK and Eire
	tileTR = tiles.deg2num(61.1856247, 2.2851563, 12) #UK and Eire

	#tileBL = tiles.deg2num(-47.279229, 107.7539063, 12) #Aus
	#tileTR = tiles.deg2num(-9.2756222, 162.5976563, 12) #Aus

	#tileBL = tiles.deg2num(50.6599084, -1.3046265, 12) #Around portsmouth, uk
	#tileTR = tiles.deg2num(50.9618867, -0.8061218, 12)

	print (tileBL, tileTR)
	count = 0
	#exit(0)
	for x in range(tileBL[0], tileTR[0] + 1):
		for y in range(tileTR[1], tileBL[1] + 1):
			print (count, (tileBL[0] - tileTR[0] + 1) * (tileTR[1] - tileBL[1] + 1), x, y)
			count += 1

			if not os.path.isdir("12"):
				os.mkdir("12")
			if not os.path.isdir("12/{0}".format(x)):
				os.mkdir("12/{0}".format(x))

			outFina = "12/{0}/{1}.osm.bz2".format(x, y)
			#outFina = "12/{0}/{1}.o5m.gz".format(x, y)
			overwrite = False
			if not os.path.exists(outFina) or overwrite:
				GetTile(x, y, 12, outFina)
				#time.sleep(1)

