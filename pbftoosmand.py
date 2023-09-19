import subprocess
import os

if __name__=="__main__":

	pth = "/home/tim/mapbuild/osmand-pbf"
	fiList = os.listdir(pth)
	fiList.sort()

	os.environ['JAVA_OPTS'] = '-Xms256M -Xmx12000M'

	for fi in fiList:

		print (fi)
		cmd = ["/home/tim/mapbuild/OsmAndMapCreator-main/utilities.sh", "generate-obf", os.path.join(pth, fi)]
		subprocess.run(cmd)


