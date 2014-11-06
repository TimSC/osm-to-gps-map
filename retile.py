
#Process osm tiles to a mkgmap template file
#nice java -jar ../mkgmap-r3337/mkgmap.jar --max-jobs=4 --drive-on-left --mapname=63290001 --description="FOSM map (C) fosm, OpenStreetMap" --copyright-message="CC BY-SA 2.0" --route --add-pois-to-areas --add-pois-to-lines --road-name-pois --index --gmapsupp -c template.args

import tiles, os, sortosm, bz2
import mergeTiles
import xml.etree.ElementTree as ET

def ProcessSingleDataTile(x, y, zoom, mapIds, tileGroups):
	fina = "../{2}/{0}/{1}.osm.bz2".format(x, y, zoom)

	mapId = 63240000+len(mapIds)
	mapIds.append(mapId)
	tileGroups.append((fina,))

	#sortosm.SortOsm(fina, "sorted.osm.bz2")
	#cmd = "java -jar ../splitter-r412/splitter.jar --mapid={0} sorted.osm.bz2".format(mapId)
	#os.system(cmd)

def MergeArea(x, y, zoom, mapIds, tileGroups):
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
	#out = bz2.BZ2File("merge.osm.bz2","w")
	#print "Found {0} data tiles".format(len(fiList))

	tileGroups.append(fiList)
	mapId = 63240000+len(mapIds)
	mapIds.append(mapId)

	if 0:
		countNodes, countWays, countRelations = mergeTiles.MergeFiles(fiList, out, 0)

		if countNodes + countWays + countRelations == 0:
			#Everything is empty
			return

		cmd = "java -jar ../splitter-r412/splitter.jar --mapid={0} merge.osm.bz2".format(mapId)
		
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

def ProcessAreaNextZoom(x, y, zoom, dataTileZoom, mapIds, tileGroups):

	lat, lon = tiles.num2deg(x, y, zoom)
	x2, y2 = tiles.deg2num(lat, lon, zoom+1)

	lat2, lon2 = tiles.num2deg(x+1, y+1, zoom)
	x3, y3 = tiles.deg2num(lat2, lon2, zoom+1)

	for cx in range(x2, x3):
		for cy in range(y2, y3):
			totalFileSize = CalcFileSize(cx, cy, zoom+1, dataTileZoom)
			if totalFileSize <= maxAllowedFileSize or zoom >= dataTileZoom:

				if zoom >= dataTileZoom:
					ProcessSingleDataTile(cx, cy, zoom+1, mapIds, tileGroups)
				else:
					#Merge at this zoom
					#print "Merge tiles", cx, cy, zoom+1, totalFileSize
					MergeArea(cx, cy, zoom+1, mapIds, tileGroups)
			else:
				#Recusively consder higher zoom level
				ProcessAreaNextZoom(cx, cy, zoom+1, dataTileZoom, mapIds, tileGroups)


if __name__=="__main__":

	#lats = (51.00434, 51.26630) #Exmoor
	#lons = (-4.02825, -3.26607) #Exmoor
	#minZoom = 8

	#lats = (49.6676278, 61.1856247) #UK and Eire
	#lons = (2.2851563, -14.765625) #UK and Eire
	#minZoom = 6

	lats = (-47.279229, -9.2756222) #Aus
	lons = (107.7539063, 162.5976563) #Aus
	minZoom = 6

	count = 0
	os.chdir("tmp")
	dataTileZoom = 12
	mapIds = []
	tileGroups = []
	maxAllowedFileSize = 10000000

	#Plan work
	print "Lat range", min(lats), max(lats)
	print "Lon range", min(lons), max(lons)
	tileBL = tiles.deg2num(min(lats), min(lons), minZoom)
	tileTR = tiles.deg2num(max(lats), max(lons), minZoom)
	print "Tile coordinates", minZoom, tileBL, tileTR
	for x in range(tileBL[0], tileTR[0] + 1):
		for y in range(tileTR[1], tileBL[1] + 1):
			totalFileSize = CalcFileSize(x, y, minZoom, dataTileZoom)
			if totalFileSize <= maxAllowedFileSize or minZoom >= dataTileZoom:

				if minZoom >= dataTileZoom:
					ProcessSingleDataTile(x, y, minZoom, mapIds, tileGroups)
				else:
					#Merge at this zoom
					#print "Merge tiles", x, y, minZoom, totalFileSize
					MergeArea(x, y, minZoom, mapIds, tileGroups)
			else:
				#Recusively consider higher zoom level
				ProcessAreaNextZoom(x, y, minZoom, dataTileZoom, mapIds, tileGroups)

	print "Numer of tile groups", len(tileGroups)

	validMapIds = []
	for i, (tg, tileId) in enumerate(zip(tileGroups, mapIds)):
		print "Process tile group", i, "of", len(mapIds), ", num files:", len(tg)
		empty = False
		if len(tg) > 1:
			out = bz2.BZ2File("tmp{0}.osm.bz2".format(tileId),"w")
			countNodes, countWays, countRelations = mergeTiles.MergeFiles(tg, out, 0)

			if countNodes + countWays + countRelations == 0:
				#Everything is empty
				empty = True
		else:
			#Check if empty
			root = ET.fromstring(bz2.BZ2File(fina).read())
			empty = True
			for nd in root:
				if nd.tag in ["node", "way", "relation"]:
					empty = False				

			if not empty:
				sortosm.SortOsm(fina, "tmp{0}.osm.bz2".format(tileId))

		if empty: continue
		validMapIds.append(tileId)

	for tileId in validMapIds:
		cmd = "java -jar ../splitter-r412/splitter.jar --mapid={0} tmp{0}.osm.bz2".format(tileId)
		os.system(cmd)

	template = "# family-id: 981\n"
	template += "# product-id: 100\n\n"
	template += "# Following is a list of map tiles.  Add a suitable description\n"
	template += "# for each one.\n\n"
	for mapId in validMapIds:
		if not os.path.isfile("{0}.osm.pbf".format(mapId)): continue
		template += "mapname: {0}\n".format(mapId)
		template += "# description: Tile\n"
		template += "input-file: {0}.osm.pbf\n".format(mapId)
	
	finaOut = open("template.args","wt")
	finaOut.write(template)
	finaOut.flush()

