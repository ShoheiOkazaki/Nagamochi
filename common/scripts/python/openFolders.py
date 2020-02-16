
import hou
import os
import subprocess

def openFolderW():
	hipPath = hou.hipFile.path()
	(hipPath, dummy) = os.path.split(hipPath)
	openFolder(hipPath)

def openFolderC():
	fxC = str(hou.getenv("CACHE"))
	seq = str(hou.getenv("SEQ"))
	shot = str(hou.getenv("SHOT"))
	user = str(hou.getenv("USER"))

	cachePath = fxC + "/" + user + "/" + seq + "/" + shot 

	#print cachePath

	# check exsit floder
	if(os.path.isdir(cachePath)):
		openFolder(cachePath)
	else:
		if hou.ui.displayMessage("'%s' does not exsit. \n\n Do you want to create a folder?" % (cachePath), buttons=("Yes", "No")) == 0:
			os.makedirs(cachePath)
			openFolder(cachePath)
	
def openFolderH():
	homePath = str(hou.getenv("HOUDINI_USER_PREF_DIR"))
	openFolder(homePath)


def openFolder(targetpath):
	#sys.platform
	print targetpath
	if os.name == 'posix':
		try:
			#os.popen( 'nemo '+ targetpath)
			subprocess.call(["nemo", targetpath])
		except:
			subprocess.call(["nautilus", targetpath])

	elif os.name == 'nt':
		targetpath = targetpath.replace('/','\\')
		os.popen( 'explorer '+ targetpath)
