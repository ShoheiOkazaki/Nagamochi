import hou

def doit(parms,type):
	parm = parms[0]
	parm_name = parm.name()
	node = parm.node()

	if type == "clear":
		parm_name = ""

	node.setUserData("descriptiveparm", parm_name)
