import xml.etree.ElementTree as ET
import bz2, sys

def SortOsm(inFina, outFina):
	fi = bz2.BZ2File(inFina)
	root = ET.fromstring(fi.read())
	fi.close()

	objDict = {}

	for obj in root:
		if 'id' in obj.attrib:
			i = int(obj.attrib['id'])
			#print obj.tag, i
			if obj.tag not in objDict:
				objDict[obj.tag] = {}
			objDict[obj.tag][i] = obj

	#for ty in objDict:
	#	print ty, len(objDict[ty]), objDict[ty].keys()

	outRoot = ET.Element("osm")
	outTree = ET.ElementTree(outRoot)
	outRoot.attrib = root.attrib

	if 'node' in objDict:	
		keys = objDict['node'].keys()
		keys.sort()
		for i in keys:
			outRoot.append(objDict['node'][i])

	if 'way' in objDict:
		keys = objDict['way'].keys()
		keys.sort()
		for i in keys:
			outRoot.append(objDict['way'][i])

	if 'relation' in objDict:
		keys = objDict['relation'].keys()
		keys.sort()
		for i in keys:
			outRoot.append(objDict['relation'][i])

	fiOut = bz2.BZ2File(outFina,"w")
	outTree.write(fiOut,"utf-8")

if __name__=="__main__":
	SortOsm(sys.argv[1], sys.argv[2])

