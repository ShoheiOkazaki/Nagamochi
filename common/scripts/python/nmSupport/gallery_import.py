import hou
import nmSupport.sop_dopimport as dopimport
import importlib
importlib.reload(dopimport)

def run(N,doptype='pyro_smoke',pane=None):

	hasTarget = False
	creatednodes_sop =[]
	creatednodes_dop =[]
	parent = None

	print(pane)


	if N:
		hasTarget = True
		parent = N.parent()

	elif pane is not None:
		parent = pane.pwd()

	if parent is None:
		print('Select any node')
		return None


	gal_dir = {
		    'pyro_smoke':['Nagamochi','SIM__pyro_smoke'],
		     'pyro_fire':['Nagamochi_Limited','SIM__pyro_fire'],
		'pyro_explosion':['Nagamochi_Limited','SIM__pyro_fire'],
		     'rbdbullet':['Nagamochi','SIM__rbdbullet'],
		'rbdbullet_emit':['Nagamochi','SIM__rbdbullet_emit'],
		}

	g_infos = gal_dir[doptype]
	g_cat = g_infos[0]
	g_name = g_infos[1] 


	gs =  hou.galleries.galleries()
	gnode = None

	for g in gs:
	    ge = g.galleryEntries(category=g_cat,name_pattern=g_name)
	    if len(ge)>0:
	    	gnode = ge[0]
	    	break

	if gnode is not None:
		cnode = gnode.createChildNode(parent)
		cnode.setComment('')

		if cnode.type().name()=='dopnet':
			cnode.parm('startframe').set(hou.expandString("$FSTART"))

		if N:
			cnode.setInput(0,N)
			cnode.moveToGoodPosition()

		elif N is None and pane:
			cnode.setPosition(pane.cursorPosition())

	else:
		print('failed')


