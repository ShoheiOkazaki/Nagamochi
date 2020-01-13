import hou

def run(N,simtype='pyro'):
	hasTarget = False
	creatednodes =[]

	if N:
		if N.type().name() == 'dopnet':
			hasTarget = True

	# --- pyro ---
	if simtype == 'pyro':
		targetNode=None
		if hasTarget:
			targetNode=N
		
		node_import,sparse = add_dopimportfield(N,targetNode=targetNode)
		creatednodes.append(node_import)
		
		node_post = add_pyropostprocess(N,sparse=sparse)
		creatednodes.append(node_post)
		node_post.setInput(0,node_import)

	# --- RBD Bullet ---
	elif simtype == 'rbd':

		targetNode=None
		if hasTarget:
			targetNode=N

		node_import = add_bulletimport(N,targetNode=targetNode)
		creatednodes.append(node_import)

	# --- set nodes's pos ---
	for node in creatednodes:
		node.moveToGoodPosition()



def add_dopimportfield(N,targetNode=None):
	parent = N.parent()

	doppath = ''
	dopnode = ''
	sparse = False

	try:
		node = parent.createNode('nmDopImportField')
	except:
		node = parent.createNode('dopimportfield')

	if targetNode != None:
		doppath = node.relativePathTo(targetNode)
		#dop_nodes = targetNode.recursiveGlob('*', hou.nodeTypeFilter.Dop,include_subnets=False)
		dop_nodes = targetNode.glob('*')
		smkobjs = []
		for dop_node in dop_nodes:
			if dop_node.type().name()=='smokeobject':
				smkobjs.append(node.relativePathTo(dop_node))
				break
			if dop_node.type().name()=='smokeobject_sparse':
				smkobjs.append(node.relativePathTo(dop_node))
				sparse = True
				break
				
		if len(smkobjs)>0:
			dopnode = smkobjs[0]
		#print node
		node.setInput(0,N)

	node.setParms({
		# base
		'doppath' : doppath,
		'dopnode' : dopnode,
		# import fileds
		'fields' : 4,
		# compression
		'compression' : 1,
		})

	flame = 'heat'
	if sparse:
		flame = 'flame'

	node.setParms({
		# import fileds
		'fieldname1' : 'density',
		'visible2'   : 'invisible',
		'fieldname2' : 'vel',
		'visible3'   : 'invisible',
		'fieldname3' : 'temperature',
		'visible4'   : 'invisible',
		'fieldname4' : flame,
		# compression
		'quantizetol1' : 0.001,	
		})

	return node,sparse

def add_pyropostprocess(N,sparse=False):
	parent = N.parent()

	node = parent.createNode('pyropostprocess')

	if sparse is False:
		node.parm('bind_flame').set('heat')

	return node
	

def add_bulletimport(N,targetNode=None):
	parent = N.parent()

	doppath = ''
	dopnode = ''

	#try:
	node = parent.createNode('nmPackedsimImport')
	# except:
	# 	node = parent.createNode('dopimportfield')

	if targetNode != None:
		doppath = node.relativePathTo(targetNode)
		dop_nodes = targetNode.glob('*')
		rbdpackedobjs = []
		for dop_node in dop_nodes:
			if dop_node.type().name()=='rbdpackedobject':
				rbdpackedobjs.append(dop_node.name())

		dopnode = ' '.join(rbdpackedobjs)

		node.setInput(0,N)

	node.setParms({
	# base
	'doppath' : doppath,
	'objpattern' : dopnode,
	# options
	'enable_deleteAttrs' : True,
	'enable_tp' : True,

	})

	return node
