import hou
import nmSupport.sop_dopimport as dopimport
reload(dopimport)

def run(N,doptype='pyro_smoke',pane=None):

	hasTarget = False
	creatednodes_sop =[]
	creatednodes_dop =[]
	parent = None

	mainName = 'SIM__{}'.format(doptype)

	if N:
		hasTarget = True
		parent = N.parent()

	elif pane is not None:
		parent = pane.pwd()


	gal_dir = {
		'pyro_smoke':['nm_sop.gal','SIM__pyro_smoke'],
		} 


	nm_root = hou.getenv('NAGAMOCHI')

	if nm_root is None:
		print 1

	
	# node_dop = parent.createNode('dopnet',mainName)


	if N:
		node_dop.setInput(0,N)
		node_dop.moveToGoodPosition()

	elif N is None and pane:
		node_dop.setPosition(pane.cursorPosition())



	# if doptype == 'pyro_smoke':
	# 	make_pyro_smoke(node_dop,hasinput=hasTarget)
	# 	dopimport.run(node_dop,simtype='pyro',pyrofire=False)

	# elif doptype == 'rbdbullet':
	# 	make_rbdbullet(node_dop,hasinput=hasTarget)

	# elif doptype == 'rbdbullet_emit':
	# 	make_rbdbullet(node_dop,hasinput=hasTarget,emit=True)




def make_pyro_smoke(node_dop,hasinput=False):
	creatednodes_dop =[]

	# - Smoke Object
	node_smkobj = node_dop.createNode('smokeobject')
	creatednodes_dop.append(node_smkobj)

	# - Resize
	node_resize = node_dop.createNode('gasresizefluiddynamic')
	creatednodes_dop.append(node_resize)
	node_resize.setParms({
		'use_tracking_objects':1,
		'tracking_path':"`opinputpath('..',0)`",
		'use_max_bounds':0
		})

	# - Volume Source
	node_vsrc   = node_dop.createNode('volumesource')
	creatednodes_dop.append(node_vsrc)
	node_vsrc.parm('numvolumes').set(3)
	node_vsrc.setParms({		
		'volume1':'density',
		'vfield1':'density',
		'volume2':'temperature',
		'vfield2':'temperature',
		'rank3':'vector',
		'volume3':'v',
		'vfield3':'vel',
		})
	if hasinput:
		node_vsrc.parm('input').set('first')

	# - Gas Dissipate
	node_dissi  = node_dop.createNode('gasdissipate')
	creatednodes_dop.append(node_dissi)
	node_dissi.setParms({
		'evaporation':0.1
		})

	# - Merge 1
	node_mg1    = node_dop.createNode('merge')
	creatednodes_dop.append(node_mg1)
	node_mg1.setInput(0,node_vsrc)
	node_mg1.setInput(1,node_dissi)

	# - Smoke Solver
	node_smkslv = node_dop.createNode('smokesolver::2.0')
	creatednodes_dop.append(node_smkslv)
	node_smkslv.setInput(0,node_smkobj)
	node_smkslv.setInput(1,node_resize)
	node_smkslv.setInput(4,node_mg1)

	# - output
	creatednodes_dop = insert_output(node_dop,node_smkslv,creatednodes_dop)

	nodes_goodpos(creatednodes_dop)


def make_rbdbullet(node_dop,hasinput=False,emit=False):
	creatednodes_dop =[]

	# - RBD Packed Object
	node_rbdobj = node_dop.createNode('rbdpackedobject')
	creatednodes_dop.append(node_rbdobj)
	if hasinput:
		node_rbdobj.parm('geosource').set('first')

	node_rbdSlv = node_dop.createNode('bulletrbdsolver')
	creatednodes_dop.append(node_rbdSlv)

	node_multSlv = node_dop.createNode('multisolver')
	creatednodes_dop.append(node_multSlv)
	node_multSlv.setInput(0,node_rbdobj)

	if emit:
		# - Sop Solver
		node_sopslv = node_dop.createNode('sopsolver','sopsolver_emit')
		#creatednodes_dop.append(node_sopslv)
		creatednodes_dop.insert(1, node_sopslv)
		# - Empty Data
		node_empty = node_dop.createNode('emptydata')
		creatednodes_dop.insert(1, node_empty)
		node_empty.parm('dataname').set('emitPack')
		node_empty.insertInput(0,node_rbdobj)
		node_multSlv.setInput(0,node_empty)
		# - Enable Solver
		node_enable = node_dop.createNode('enablesolver')
		creatednodes_dop.insert(3, node_enable)
		node_enable.parm('enabledata').set('emitPack')
		node_enable.setInput(0,node_sopslv)
		
		node_multSlv.setInput(1,node_enable)
		node_multSlv.setInput(2,node_rbdSlv)

		
	else:
		node_multSlv.setInput(1,node_rbdSlv)

	node_forceG = node_dop.createNode('gravity')
	creatednodes_dop.append(node_forceG)
	node_forceG.setInput(0,node_multSlv)


	# - Merge 1
	node_mg1    = node_dop.createNode('merge')
	creatednodes_dop.append(node_mg1)
	node_mg1.setInput(0,node_forceG)

	# - output
	creatednodes_dop = insert_output(node_dop,node_mg1,creatednodes_dop)

	nodes_goodpos(creatednodes_dop)


def insert_output(node_dop,inputnode,creatednodes_dop):
	node_output = hou.node('{}/output'.format(node_dop.path()))
	node_output.setInput(0,inputnode)
	creatednodes_dop.append(node_output)

	return creatednodes_dop

def nodes_goodpos(creatednodes):
	for node in creatednodes:
		node.moveToGoodPosition()



