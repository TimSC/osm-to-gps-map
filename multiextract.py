import os
import subprocess

if __name__=="__main__":

	if not os.path.exists("extracts"):
		os.mkdir("extracts")

	for area in os.listdir("regions"):
		print (area)
	
		areaSplit = os.path.splitext(area)
		cmd = ["./extract", "--wkt={}".format(os.path.join("regions", area)), "--out={}".format(os.path.join("regions", "{}.o5m.gz".format(areaSplit[0])))]
		print (cmd)
		subprocess.run(cmd)
		#os.system(" ".join(cmd))


