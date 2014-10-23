import math, os, bz2, urlutil, tiles, shutil

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

	print tileBL, tileTR
	count = 0
	outFolder = "uk-and-ireland"
	#exit(0)
	for x in range(tileBL[0], tileTR[0] + 1):
		for y in range(tileTR[1], tileBL[1] + 1):
			print count, (tileBL[0] - tileTR[0] + 1) * (tileTR[1] - tileBL[1] + 1), x, y
			count += 1

			inFina = "12/{0}/{1}.osm.bz2".format(x, y)
			if not os.path.isfile(inFina):
				print "File not found",inFina
				exit(0)

			if not os.path.isdir(outFolder+"/12"):
				os.mkdir(outFolder+"/12")
			if not os.path.isdir(outFolder+"/12/{0}".format(x)):
				os.mkdir(outFolder+"/12/{0}".format(x))
			outFina = outFolder+"/12/{0}/{1}.osm.bz2".format(x, y)

			shutil.copyfile(inFina, outFina)

	print "All done!"

