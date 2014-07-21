
#Process osm tiles to a mkgmap template file
#java -jar mkgmap-r2638/mkgmap.jar --gmapsupp -c template.args

import tiles, os, sortosm

if __name__=="__main__":

	#tileBL = tiles.deg2num(51.7882364, -3.4765251, 12)
	#tileTR = tiles.deg2num(52.3707994, -2.2782056, 12)

	tileBL = tiles.deg2num(51.00434, -4.02825, 12) #Exmoor
	tileTR = tiles.deg2num(51.26630, -3.26607, 12) #Exmoor

	print tileBL, tileTR
	count = 0

	mapIds = []
	for x in range(tileBL[0], tileTR[0] + 1):
		for y in range(tileTR[1], tileBL[1] + 1):
			fina = "12/{0}/{1}.osm.bz2".format(x, y)
			sortosm.SortOsm(fina, "sorted.osm.bz2")

			mapId = 63240000+count
			cmd = "java -jar splitter-r304/splitter.jar --mapid={0} sorted.osm.bz2".format(mapId)
			mapIds.append(mapId)
			os.system(cmd)
			count += 1

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

