import math, os, bz2, urlutil, tiles

def GetTile(x, y, zoom, outFina):
	
	topLeft = tiles.num2deg(x, y, zoom)
	bottomRight = tiles.num2deg(x+1, y+1, zoom)

	url = "http://fosm.org/api/0.6/map?bbox={0},{1},{2},{3}".format(topLeft[1],bottomRight[0],bottomRight[1],topLeft[0])
	print url
	
	body, header = urlutil.Get(url)
	responseCode = urlutil.HeaderResponseCode(header)
	print responseCode
	if responseCode != "HTTP/1.1 200 OK":
		return 0
	
	outFi = bz2.BZ2File(outFina,"w")
	outFi.write(body)
	return 1

tileBL = tiles.deg2num(51.7882364, -3.4765251, 12)
tileTR = tiles.deg2num(52.3707994, -2.2782056, 12)

print tileBL, tileTR
count = 0

for x in range(tileBL[0], tileTR[0] + 1):
	for y in range(tileTR[1], tileBL[1] + 1):
		print count, (tileBL[0] - tileTR[0] + 1) * (tileTR[1] - tileBL[1] + 1), x, y
		count += 1

		if not os.path.isdir("12"):
			os.mkdir("12")
		if not os.path.isdir("12/{0}".format(x)):
			os.mkdir("12/{0}".format(x))

		outFina = "12/{0}/{1}.osm.bz2".format(x, y)
		if not os.path.exists(outFina):
			GetTile(x, y, 12, outFina)
		
