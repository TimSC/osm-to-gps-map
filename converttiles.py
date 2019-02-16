from __future__ import print_function
import os

def ProcessPath(pthIn, pthOut):
	for fina in os.listdir(pthIn):
		pthIn2 = os.path.join(pthIn, fina)
		pthOut2 = os.path.join(pthOut, fina)

		if os.path.isdir(pthIn2):
			ProcessPath(pthIn2, pthOut2)
		else:
			print (pthIn2)
			dirOut2 = os.path.dirname(pthOut2)
			if not os.path.exists(dirOut2):
				os.makedirs(dirOut2)

			pthOutBase2 = os.path.splitext(os.path.splitext(pthOut2)[0])[0]
			cmd = "bzcat {} | osmconvert - --out-pbf > {}.pbf".format(pthIn2, pthOutBase2)
			os.system(cmd)

if __name__=="__main__":
	ProcessPath("/home/tim/dev/mapdev/wight/12osmgz", "/home/tim/dev/mapdev/wight/12")
	
