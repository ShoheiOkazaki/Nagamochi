import hou

def run(n,choice):
	n_pos = n.position()
	n_outs = n.outputs()

	pos = n_pos - hou.Vector2(0,1)


	if choice==0:
		nn = createTimeBlend(n)
	else:
		nn = createSwitchOff(n)
	nn.setPosition( pos )
	nn.setInput( 0,n )


	if len(n_outs)>0:
		for n_out in n_outs:
			from_n =  n_out.inputs().index(n)
			n_out.setInput( from_n,nn )
	print("[Nagamochi][Python][createCtrlReadFile4Cache] Create '%s' under '%s'." % ( nn.name(),n.name() ))


def createTimeBlend(n):
	tb = n.parent().createNode( 'timeblend' )
	tb.setParmExpressions({
		'firstframe': 'ch("../%s/f1")' % n.name(),
		'lastframe': 'ch("../%s/f2")' % n.name(),
		})
	return tb


def createSwitchOff(n):
	so = n.parent().createNode( 'nmSwitchOff' )
	so.parm('rangeList').set(2)
	so.setParms({
		'type'  : 1,
		'mode1' : '',
		'mode2' : '&&',
		'sign1' : '>=',
		'sign2' : '<='
		})
	so.setParmExpressions({
		'targetB1' : 'ch("../%s/f1")' % n.name(),
		'targetB2' : 'ch("../%s/f2")' % n.name(),
		})
	return so