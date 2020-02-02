import hou

def get_ramp_parm(n):
	ps_name = []
	ps_label = []

	parm_group = n.parmTemplateGroup()
	parm_tmps =  n.parms()

	for p in parm_tmps:
		pt =  p.parmTemplate()
		if pt.dataType() == hou.parmData.Ramp:
			if p.isVisible():
				ps_name.append(pt.name())
				ps_label.append('{}({})'.format(pt.label(),pt.name()))
			
	return ps_name,ps_label


def invert_parm(n,parmname):
	parm = hou.parm('{}/{}'.format(n.path(),parmname))
	ramp = parm.evalAsRamp()

	ramp_isColor = ramp.isColor()
	ramp_keys = ramp.keys()
	ramp_vals = ramp.values()
	ramp_basis = ramp.basis()

	ramp_keysl = list(reversed(list(ramp_keys)))
	invert_keys = []
	for ramp_key in ramp_keysl:
		invert_keys.append(1-float(ramp_key))

	invert_vals = list(reversed(list(ramp_vals)))
	invert_basis = list(reversed(list(ramp_basis)))

	ramp_parms = hou.Ramp(tuple(invert_basis),tuple(invert_keys),tuple(invert_vals))

	parm.set(ramp_parms)


def run(n):
	ramp_parms_name,ramp_parms_label = get_ramp_parm(n)

	sel_parms = hou.ui.selectFromList(ramp_parms_label, default_choices=([0]),title="[Nagamochi] Reverse Ramp",message='Select Parms to reverse ramp on [{}]'.format(n.path()))

	for ramp_parm in sel_parms:
		invert_parm(n,ramp_parms_name[ramp_parm])
	