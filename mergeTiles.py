import bz2, os
import xml.etree.ElementTree as ET
import slippytiles

def MergeFile(fina, ty, existing, fiOut):
	fi = bz2.BZ2File(fina)
	root = ET.fromstring(fi.read())

	for el in root:
		if el.tag != ty: continue
		objId = int(el.attrib['id'])
		if objId in existing: 
			print "skipping", el.tag, objId
			continue
		print el.tag, objId
		existing.add(objId)

		xml = ET.tostring(el, encoding="utf-8")
		fiOut.write(xml)

def CopyObjsOfTypeByWalking(pth, ty, fiOut, existing):
	
	for fi in os.listdir(pth):
		if os.path.isdir(pth+"/"+fi):
			CopyObjsOfTypeByWalking(pth+"/"+fi, ty, fiOut, existing)

		if os.path.isfile(pth+"/"+fi):
			print pth+"/"+fi

			MergeFile(pth+"/"+fi, ty, existing, fiOut)

if __name__=="__main__":
	
	out = bz2.BZ2File("merge.osm.bz2","w")
	#out = open("merge.osm","wt")
	out.write("<?xml version='1.0' encoding='UTF-8'?>\n")
	out.write("<osm version='0.6' upload='true' generator='py'>\n")

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

	existing = set()
	#MergeFile("aux.osm.bz2", "node", existing, out)
	for fina in fiList:
		MergeFile(fina, "node", existing, out)
	#CopyObjsOfTypeByWalking("existing/12", "node", out, existing)

	existing = set()
	#MergeFile("aux.osm.bz2", "way", existing, out)
	for fina in fiList:
		MergeFile(fina, "way", existing, out)
	#CopyObjsOfTypeByWalking("existing/12", "way", out, existing)

	existing = set()
	#MergeFile("aux.osm.bz2", "relation", existing, out)
	for fina in fiList:
		MergeFile(fina, "relation", existing, out)
	#CopyObjsOfTypeByWalking("existing/12", "relation", out, existing)

	out.write("</osm>\n")
	out.close()


