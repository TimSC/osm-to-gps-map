
#Process osm tiles to a mkgmap template file
#java -jar mkgmap-r2638/mkgmap.jar --gmapsupp -c template.args

import tiles, os, sortosm, bz2
import mergeTiles
import xml.etree.ElementTree as ET

def ProcessSingleDataTile(x, y, zoom, mapIds):
	fina = "../{2}/{0}/{1}.osm.bz2".format(x, y, zoom)

	#Check if empty
	root = ET.fromstring(bz2.BZ2File(fina).read())
	found = False
	for nd in root:
		if nd.tag in ["node", "way", "relation"]:
			found = True				
	if not found: return

	sortosm.SortOsm(fina, "sorted.osm.bz2")

	mapId = 63240000+len(mapIds)
	cmd = "java -jar ../splitter-r412/splitter.jar --mapid={0} sorted.osm.bz2".format(mapId)
	mapIds.append(mapId)
	os.system(cmd)

def MergeArea(x, y, zoom, mapIds):
	lat, lon = tiles.num2deg(x, y, zoom)
	x2, y2 = tiles.deg2num(lat, lon, dataTileZoom)

	lat2, lon2 = tiles.num2deg(x+1, y+1, zoom)
	x3, y3 = tiles.deg2num(lat2, lon2, dataTileZoom)

	fiList = []
	for cx in range(x2, x3):
		for cy in range(y2, y3):
			fina = "../12/{0}/{1}.osm.bz2".format(cx, cy)
			if not os.path.isfile(fina):
				continue
			fiList.append(fina)

	if len(fiList) == 0:
		return
	out = bz2.BZ2File("merge.osm.bz2","w")
	print "Found {0} data tiles".format(len(fiList))
	countNodes, countWays, countRelations = mergeTiles.MergeFiles(fiList, out, 0)

	if countNodes + countWays + countRelations == 0:
		#Everything is empty
		return

	mapId = 63240000+len(mapIds)
	cmd = "java -jar ../splitter-r412/splitter.jar --mapid={0} merge.osm.bz2".format(mapId)
	mapIds.append(mapId)
	os.system(cmd)

def CalcFileSize(x, y, zoom, dataTileZoom):
	lat, lon = tiles.num2deg(x, y, zoom)
	x2, y2 = tiles.deg2num(lat, lon, dataTileZoom)

	lat2, lon2 = tiles.num2deg(x+1, y+1, zoom)
	x3, y3 = tiles.deg2num(lat2, lon2, dataTileZoom)

	#print (x2, x3), (y2, y3)
	totalSize = 0
	for cx in range(x2, x3):
		for cy in range(y2, y3):
			fina = "../12/{0}/{1}.osm.bz2".format(cx, cy)
			if not os.path.isfile(fina):
				continue
			s = os.path.getsize(fina)
			totalSize += s
	return totalSize

def ProcessAreaNextZoom(x, y, zoom, dataTileZoom, mapIds):
	lat, lon = tiles.num2deg(x, y, zoom)
	x2, y2 = tiles.deg2num(lat, lon, zoom+1)

	lat2, lon2 = tiles.num2deg(x+1, y+1, zoom)
	x3, y3 = tiles.deg2num(lat2, lon2, zoom+1)

	for cx in range(x2, x3):
		for cy in range(y2, y3):
			totalFileSize = CalcFileSize(cx, cy, zoom+1, dataTileZoom)
			if totalFileSize <= maxAllowedFileSize or zoom >= dataTileZoom:

				if zoom >= dataTileZoom:
					ProcessSingleDataTile(cx, cy, zoom+1, mapIds)
				else:
					#Merge at this zoom
					print "Merge tiles", cx, cy, zoom+1, totalFileSize
					MergeArea(cx, cy, zoom+1, mapIds)
			else:
				#Recusively consder higher zoom level
				ProcessAreaNextZoom(cx, cy, zoom+1, dataTileZoom, mapIds)


if __name__=="__main__":

	#tileBL = tiles.deg2num(51.7882364, -3.4765251, 12)
	#tileTR = tiles.deg2num(52.3707994, -2.2782056, 12)

	lats = (51.00434, 51.26630) #Exmoor
	lons = (-4.02825, -3.26607) #Exmoor

	#tileBL = tiles.deg2num(49.6676278, -14.765625, 12) #UK and Eire
	#tileTR = tiles.deg2num(61.1856247, 2.2851563, 12) #UK and Eire

	count = 0
	os.chdir("tmp")
	dataTileZoom = 12
	minZoom = 8
	mapIds = []
	maxAllowedFileSize = 10000000

	tileBL = tiles.deg2num(min(lats), min(lons), minZoom)
	tileTR = tiles.deg2num(max(lats), max(lons), minZoom)
	print minZoom, tileBL, tileTR
	for x in range(tileBL[0], tileTR[0] + 1):
		for y in range(tileTR[1], tileBL[1] + 1):
			totalFileSize = CalcFileSize(x, y, minZoom, dataTileZoom)
			if totalFileSize <= maxAllowedFileSize or minZoom >= dataTileZoom:

				if zoom >= dataTileZoom:
					ProcessSingleDataTile(x, y, minZoom, mapIds)
				else:
					#Merge at this zoom
					print "Merge tiles", x, y, minZoom, totalFileSize
					MergeArea(x, y, minZoom, mapIds)
			else:
				#Recusively consder higher zoom level
				ProcessAreaNextZoom(x, y, minZoom, dataTileZoom, mapIds)

	template = "# family-id: 981\n"
	template += "# product-id: 100\n\n"
	template += "# Following is a list of map tiles.  Add a suitable description\n"
	template += "# for each one.\n\n"
	for mapId in mapIds:
		if not os.path.isfile("{0}.osm.pbf".format(mapId)): continue
		template += "mapname: {0}\n".format(mapId)
		template += "# description: Tile\n"
		template += "input-file: {0}.osm.pbf\n".format(mapId)
	
	finaOut = open("template.args","wt")
	finaOut.write(template)
	finaOut.flush()

