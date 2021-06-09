
import hou
import os
import subprocess

from nagamochi_utils import MSG
script_name = 'OpenFolder'

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

def getFolderParms(node):

	chooselist = []
	targets = {}

	for parm in node.parms():
		if  parm.parmTemplate().type() == hou.parmTemplateType.String:
			if parm.parmTemplate().stringType() == hou.stringParmType.FileReference and parm.eval() is not '':
				chooselist.append( '{} - {}({})'.format(node.path(),parm.parmTemplate().label(),parm.name()) )
				# targets.append( os.path.dirname(parm.eval()) )
				# targets.append( '{} - {}({})'.format(node.path(),parm.parmTemplate().label(),parm.name()) )
				targets["{} - {}({})".format(node.path(),parm.parmTemplate().label(),parm.name())] = os.path.dirname(parm.eval())

	return chooselist,targets

def openFolderFromSelectedNodes(ns=hou.selectedNodes()):

	chooselist = []
	choosedict = {}

	for n in ns:
		getlist,getdict = getFolderParms(n)
		chooselist += getlist
		choosedict.update(getdict)

	if len(chooselist)>0:
		choose = hou.ui.selectFromList(chooselist, message='Select Parms to bake key')

		for i in choose:
			foloderpath = choosedict[chooselist[i]]
			if os.path.exists(foloderpath):
				openFolder(foloderpath)
			else:
				meg_txt ='{} is does not exists.'.format(foloderpath)
				MSG(script_name,meg_txt,StatusMessage_enbale=True,StatusMessage_type=hou.severityType.ImportantMessage)

def openFolder(targetpath):
	if os.name == 'posix':
		try:
			#os.popen( 'nemo '+ targetpath)
			subprocess.call(["xdg-open", targetpath])
		except:
			subprocess.call(["nemo", targetpath])

	elif os.name == 'nt':
		targetpath = targetpath.replace('/','\\')
		os.popen( 'explorer '+ targetpath)
