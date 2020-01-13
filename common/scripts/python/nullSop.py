import hou

#hou.pwd().setColor(hou.Color((.8,.8,.8))); hou.pwd().setName("null1", True)
def setNodeNameColor():
    n = hou.pwd()
    presets = {
                "DISPLAY": [hou.Color((0.0,0.4,1.0)), "Display"],
                "RENDER" : [hou.Color((0.4,0.2,0.6)), "Render"],
                "OUT"    : [hou.Color((0.1,0.1,0.1)), ""],
                "NULL"   : [hou.Color((0.2,0.2,0.2)), "Both"],
                "TO_REN_": [hou.Color((0.4,0.2,0.6)), ""],
                "TO_DOP_": [hou.Color((0.4,0.2,0.6)), ""],
                }

    prefix  = n.parm('output_prefix').eval()
    rentype = n.parm('output_ren_type').eval()
    doptype = n.parm('output_dop_type').eval()
    label   = n.parm('output_label').eval().replace(' ','_')
    
    arg = presets[prefix]
    name = ""

    if prefix=="DISPLAY":
        name = prefix
        if len(label)>0:
            name += '_%s' % label

    elif prefix=="RENDER":
        name = prefix
        if len(label)>0:
            name += '_%s' % label

    elif prefix=="OUT":
        name = prefix
        if len(label)>0:
            name += '_%s' % label

    elif prefix=="NULL":
        name = prefix
        if len(label)>0:
            name += '_%s' % label

    elif prefix=="TO_REN_":
        name = '%s_%s_%s' % (prefix,rentype,label)

    elif prefix=="TO_DOP_":
        name = '%s_%s_%s' % (prefix,doptype,label)

    else:
        pass
    
    n.setName(name)
    n.setColor(arg[0])

    if arg[1]=="Display":
        n.setDisplayFlag(True)
    elif arg[1]=="Render":
        n.setRenderFlag(True)
    elif arg[1]=="Both":
        n.setDisplayFlag(True)
        n.setRenderFlag(True)
    else:
        pass

                                