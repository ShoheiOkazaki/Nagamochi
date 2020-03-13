import hou

def run(pane):
	
	node = hou.node('/obj').createNode('geo','work_')
	node.setPosition(pane.cursorPosition())

	lockattrs = [
		'tx','ty','tz',
		'rx','ry','rz',
		'sx','sy','sz',
		'px','py','pz',
		'prx','pry','prz',
		'scale'
		]

	for attr in lockattrs:
		node.parm(attr).lock(True)

	node.setSelectableInViewport(False)
