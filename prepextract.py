import os
import tempfile
import subprocess
from renumberfosm import RenumberFosmFile

if __name__=="__main__":

	pth = "/var/www/pycrocosm/pgmap/regions"
	finaLi = os.listdir(pth)
	finaLi.sort()

	tmpDir = tempfile.TemporaryDirectory()

	for fina in finaLi:

		finaSplit = os.path.splitext(fina)
		if finaSplit[1] != ".gz": continue
		#if fina != "Ireland,_Dublin.o5m.gz": continue
		print (fina)

		outFina = finaSplit[0]+".pbf"
		if os.path.exists(outFina):
			continue

		renumFina = os.path.join(tmpDir.name, fina)
		RenumberFosmFile(os.path.join(pth, fina), renumFina)

		outFina = outFina.replace(".o5m.pbf", ".osm.pbf")

		pbfFina = os.path.join("/home/tim/mapbuild/osmand-pbf", outFina)
		subprocess.run(["osmconvert", renumFina, "-o={}".format(pbfFina)])

		os.unlink(renumFina)

