from pyo5m import o5m
import gzip, sys, json

#Used to renumber ways as OsmAnd map creator does not like 64-bit ways

class MinMaxObjects(object):
	def __init__(self):
		self.minNodeId = None
		self.minWayId = None
		self.minRelationId = None
		self.maxNodeId = None
		self.maxWayId = None
		self.maxRelationId = None
		self.countNodes = 0
		self.countWays = 0
		self.countRelations = 0

	def __del__(self):
		pass

	def StoreIsDiff(self, isDiff):
		pass

	def StoreBounds(self, bbox):
		pass

	def StoreNode(self, objectId, metaData, tags, pos):
		#if objectId > 0x7FFFFFFF: return
		#if objectId >= 2000000000000: return
		if self.minNodeId is None or objectId < self.minNodeId:
			self.minNodeId = objectId
		if self.maxNodeId is None or objectId > self.maxNodeId:
			self.maxNodeId = objectId

	def StoreWay(self, objectId, metaData, tags, refs):
		#if objectId > 0x7FFFFFFF: return
		#if objectId >= 2000000000000: return
		if self.minWayId is None or objectId < self.minWayId:
			self.minWayId = objectId
		if self.maxWayId is None or objectId > self.maxWayId:
			self.maxWayId = objectId

	def StoreRelation(self, objectId, metaData, tags, refs):
		#if objectId > 0x7FFFFFFF: return
		#if objectId >= 2000000000000: return
		if self.minRelationId is None or objectId < self.minRelationId:
			self.minRelationId = objectId
		if self.maxRelationId is None or objectId > self.maxRelationId:
			self.maxRelationId = objectId

if __name__ == "__main__":

	filt = MinMaxObjects()

	if len(sys.argv) < 3:
		print ("Requires at least 2 args")
		exit(-1)

	for finaIn in sys.argv[1:-1]:
		print (finaIn)

		fiIn = gzip.open(finaIn, "rb")

		dec = o5m.O5mDecode(fiIn)

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

	out = {}
	out['minNodeId'] = filt.minNodeId
	out['maxNodeId'] = filt.maxNodeId
	out['minWayId'] = filt.minWayId
	out['maxWayId'] = filt.maxWayId
	out['minRelationId'] = filt.minRelationId
	out['maxRelationId'] = filt.maxRelationId
	print (out)

	del filt

	fi = open(sys.argv[-1], "wt")
	json.dump(out, fi)
	fi.close()

