from pyo5m import o5m
import gzip, sys

#Used to renumber ways as OsmAnd map creator does not like 64-bit ways

#For the original fork from OSM (32-bit IDs): {'minNodeId': 1, 'maxNodeId': 1588236629, 'minWayId': 35, 'maxWayId': 145404394, 'minRelationId': 11, 'maxRelationId': 1966857}
#IDs for the GT.M era of FOSM: {'minNodeId': 1000000000009, 'maxNodeId': 1000596439518, 'minWayId': 1000000000002, 'maxWayId': 1000002628510, 'minRelationId': 1000000000003, 'maxRelationId': 1000000155568}
#IDs for the pycrocosm era of FOSM start at 2000000000000

def ConvertNodeId(objId):
	if objId <= 1588236629:
		return objId
	if objId < 1000000000000:
		raise ValueError("ID in unexpected range")
	if objId <= 1000596439518:
		return objId - 1000000000000 + 1600000000
	if objId < 2000000000000:
		raise ValueError("ID in unexpected range")
	return objId - 2000000000000 + 2200000000

def ConvertWayId(objId):
	if objId <= 145404394:
		return objId
	if objId < 1000000000000:
		raise ValueError("ID in unexpected range")
	if objId <= 1000002628510:
		return objId - 1000000000000 + 150000000
	if objId < 2000000000000:
		raise ValueError("ID in unexpected range")
	return objId - 2000000000000 + 160000000

def ConvertRelationId(objId):
	if objId <= 1966857:
		return objId
	if objId < 1000000000000:
		raise ValueError("ID in unexpected range")
	if objId <= 1000000155568:
		return objId - 1000000000000 + 2000000
	if objId < 2000000000000:
		raise ValueError("ID in unexpected range")
	return objId - 2000000000000 + 2200000

class RenumberFosm(object):
	def __init__(self, output):
		self.output = output
		self.prevType = None
		self.countNodes = 0
		self.countWays = 0
		self.countRelations = 0

	def __del__(self):
		self.output.Finish()

	def StoreIsDiff(self, isDiff):
		self.output.StoreIsDiff(isDiff)

	def StoreBounds(self, bbox):
		self.output.StoreBounds(bbox)

	def StoreNode(self, objectId, metaData, tags, pos):
		if self.prevType is not None and self.prevType != "n":
			self.output.Reset()
		self.output.StoreNode(objectId, metaData, tags, pos)
		self.prevType = "n"
		self.countNodes += 1
		#if self.countNodes % 1000 == 0:
		#	print (self.countNodes)

	def StoreWay(self, objectId, metaData, tags, refs):
		if self.prevType is not None and self.prevType != "w":
			self.output.Reset()
		self.output.StoreWay(ConvertWayId(objectId), metaData, tags, refs)
		self.prevType = "w"
		self.countWays += 1
		#if self.countWays % 1000 == 0:
		#	print (self.countWays)

	def StoreRelation(self, objectId, metaData, tags, refs):
		if self.prevType is not None and self.prevType != "r":
			self.output.Reset()

		remappedRefs = []
		for typeStr, refId, role in refs:
			if typeStr == "node":
				remappedRefs.append((typeStr, refId, role))
			elif typeStr == "way":
				remappedRefs.append((typeStr, ConvertWayId(refId), role))
			elif typeStr == "relation":
				remappedRefs.append((typeStr, ConvertRelationId(refId), role))

		self.output.StoreRelation(ConvertRelationId(objectId), metaData, tags, remappedRefs)

		self.prevType = "r"
		self.countRelations += 1
		#if self.countRelations % 1000 == 0:
		#	print (self.countRelations)

def RenumberFosmFile(finaIn, finaOut):
	fiIn = gzip.open(finaIn, "rb")
	fiOut = gzip.open(finaOut, "wb")

	dec = o5m.O5mDecode(fiIn)
	enc = o5m.O5mEncode(fiOut)
	filt = RenumberFosm(enc)

	dec.funcStoreNode = filt.StoreNode
	dec.funcStoreWay = filt.StoreWay
	dec.funcStoreRelation = filt.StoreRelation
	dec.funcStoreBounds = filt.StoreBounds
	dec.funcStoreIsDiff = filt.StoreIsDiff
	dec.DecodeHeader()

	eof = False
	while not eof:
		eof = dec.DecodeNext()

	del dec
	del filt
	del enc

	fiOut.close()


if __name__ == "__main__":

	finaIn = "uk-eire-fosm-2017-jan.o5m.gz"
	finaOut = "renumbered.o5m.gz"

	if len(sys.argv) >= 2:
		finaIn = sys.argv[1]
	if len(sys.argv) >= 3:
		finaOut = sys.argv[2]

	RenumberFosmFile(finaIn, finaOut)

