import bz2, os
import xml.etree.ElementTree as ET
import slippytiles

def MergeFile(fina, ty, existing, fiOut, verbose = 1):
	fi = bz2.BZ2File(fina)
	try:
		root = ET.fromstring(fi.read())
	except ET.ParseError as err:
		print "Xml parsing error in", fina
		return 0

	count = 0

	for el in root:
		if el.tag != ty: continue
		objId = int(el.attrib['id'])
		if objId in existing: 
			if verbose >= 1:
				print "skipping", el.tag, objId
			continue
		if verbose >= 1:
			print el.tag, objId
		existing.add(objId)
		count += 1

		xml = ET.tostring(el, encoding="utf-8")
		fiOut.write(xml)

	return count

def CopyObjsOfTypeByWalking(pth, ty, fiOut, existing):
	
	for fi in os.listdir(pth):
		if os.path.isdir(pth+"/"+fi):
			CopyObjsOfTypeByWalking(pth+"/"+fi, ty, fiOut, existing)

		if os.path.isfile(pth+"/"+fi):
			print pth+"/"+fi

			MergeFile(pth+"/"+fi, ty, existing, fiOut)

def MergeFiles(fiList, out, verbose = 1):

	out.write("<?xml version='1.0' encoding='UTF-8'?>\n")
	out.write("<osm version='0.6' upload='true' generator='py'>\n")

	countNodes = 0
	countWays = 0
	countRelations = 0

	existing = set()
	for fina in fiList:
		countNodes += MergeFile(fina, "node", existing, out, verbose)

	existing = set()
	for fina in fiList:
		countWays += MergeFile(fina, "way", existing, out, verbose)

	existing = set()
	for fina in fiList:
		countRelations += MergeFile(fina, "relation", existing, out, verbose)

	out.write("</osm>\n")
	out.close()

	return countNodes, countWays, countRelations

if __name__=="__main__":
	
	#lats, lons = [51.383075,50.705752], [-1.955713,-0.729294]
	#lats, lons = [51.26630,51.00434], [-3.26607,-4.02825] #Exmoor
	#lats, lons = [49.0018439,49.3644891], [-0.6632996,0.0054932] #Caen
	lats, lons = [27.673799,31.297328], [32.1679688,35.0024414] #Sinai

	zoom = 12
	xtile1, ytile1 = slippytiles.deg2num(min(lats), min(lons), zoom)
	xtile2, ytile2 = slippytiles.deg2num(max(lats), max(lons), zoom)
	collectLat, collectLon = [], []
	
	fiList = []
	for x in range(xtile1, xtile2+1):
		for y in range(ytile2, ytile1+1):
			rootPath = "12"
			dirName = rootPath+"/"+str(x)
			fina = dirName+"/"+str(y)+".osm.bz2"
			if os.path.isfile(fina):
				fiList.append(fina)

	out = bz2.BZ2File("merge.osm.bz2","w")
	#out = open("merge.osm","wt")
	MergeFiles(fiList, out)

