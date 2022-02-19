import hou

def switchOpenCl(slnode,value):

    dopnodes = slnode.children()
    checknodes = dopnodes
    i = len(dopnodes)
    t = 0  
    
    while i > 0:
        dopnode = dopnodes[t]
        if dopnode.isLockedHDA()!=True and len(dopnode.children())!=0:
            dopnodes += dopnode.children()
            i += len(dopnode.children())
        else:
            if dopnode.parm('opencl'):
                if dopnode.parm('opencl').path() == dopnode.parm('opencl').getReferencedParm().path():
                    dopnode.parm('opencl').set(value)
                    print(dopnode.path())            
        t += 1
        i -= 1


def run():
	slnode = hou.selectedNodes()[0]
	if slnode.type().name()=='dopnet':
	    uiText = 'Change OpenCL value on all children nodes in this %s' % slnode.path()
	    value = hou.ui.displayMessage(title='OpenCL', text=uiText, buttons=("Deactive", "Active"))
	    switchOpenCl(slnode,value)
