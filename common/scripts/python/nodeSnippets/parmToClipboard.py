import hou

def run(parm,outtype):
	#parm = kwargs.get("parms", None)[0]

	if outtype == 'path':
		return hou.ui.copyTextToClipboard(parm.path())
	elif outtype == 'name':
		return hou.ui.copyTextToClipboard(parm.name())
	elif outtype == 'value':
		return hou.ui.copyTextToClipboard(parm.eval())