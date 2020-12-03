import os
import subprocess

if __name__=="__main__":

	pth = '/var/www/pycrocosm/pgmap'

	extractsPth = os.path.join(pth, "extracts")
	if not os.path.exists(extractsPth):
		os.mkdir(extractsPth)

	regionsPth = "/home/tim/dev/osm-to-gps-map/regions"
	listDir = os.listdir(regionsPth)
	listDir.sort()
	for area in listDir:
		print (area)
		areaSplit = os.path.splitext(area)
		if areaSplit[1] != ".wkt": continue
	
		outFina = os.path.join(extractsPth, "{}.o5m.gz".format(areaSplit[0]))
		if os.path.exists(outFina):
			continue
		cmd = ["./extract", "--wkt={}".format(os.path.join(regionsPth, area)), "--out={}".format(outFina)]
		print (cmd)
		subprocess.run(cmd, cwd=pth)
		os.system(" ".join(cmd))


