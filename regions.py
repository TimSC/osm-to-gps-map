#Process data from https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-1-states-provinces/
import os
import csv
import sys
from shapely.wkt import dumps, loads

if __name__=="__main__":

	csv.field_size_limit(sys.maxsize)
	csv = csv.DictReader(open("/home/tim/Downloads/ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.wkt/ne_10m_admin_1_states_provinces.csv", "rt"))
	geounits = {}

	if not os.path.exists("regions"):
		os.mkdir("regions")

	for li in csv:

		gu = li['geonunit']
		if gu not in geounits:
			geounits[gu] = {}
		region = li['region']
		if region not in geounits[gu]:
			geounits[gu][region] = {}
		
		nameId = li['name_id']

		wkt = loads(li['WKT'])
		geounits[gu][region][nameId] = (li, wkt)

	#for gu in geounits:
	#	print (gu)

	for geounit in ['England', 'Scotland', 'Wales', 'Northern Ireland', 'Ireland']:

		for region in geounits[geounit]:
			regionList = geounits[geounit][region]

			combined = None
			for nameId in regionList:
				li, wkt = regionList[nameId]
				if combined is None:
					combined = wkt
				else:
					combined = combined.union(wkt)

			combined = combined.buffer(0.01)
			combined = combined.simplify(0.0001)

			print (geounit, region, combined.area)

			fina = "{}, {}.wkt".format(geounit, region).replace(" ", "_")
			fi=open(os.path.join("regions", fina), "wt")
			fi.write(dumps(combined))
			fi.close()

