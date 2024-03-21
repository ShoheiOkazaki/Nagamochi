import hou


# import hou
# import createReadFile,nagamochi_utils
# nagamochi_utils.reload_func(createReadFile)
# n = hou.node('/obj/geo1/nmFileCache1')

# print(n.type().nameComponents()[2])

# createReadFile.run(n)


def create_read_node(parent, node_name, version, position, path, is_wedge, parmnum):

    node_type = 'file' if not is_wedge else 'nmFileMerge'
    node = parent.createNode(node_type, f'{node_type}__{node_name}_{version}')
    node.setPosition(position + hou.Vector2(2, -1))

    addVerParm = eval('hou.%sParmTemplate("%s", "%s", 1,default_value=(["%s"]))' % ('String', 'version', 'Version ', 'v001'))
    addSrcParm = hou.StringParmTemplate("source", "Source", 1, string_type=hou.stringParmType.NodeReference)

    parm = node.parms()[parmnum[0]]
    parmTmp = parm.parmTemplate()
    parmGroup = node.parmTemplateGroup()
    parmIndex = parmGroup.findIndices(parmTmp.name())[0]
    parmGroup.insertAfter(parmGroup.parmTemplates()[parmIndex],addVerParm)
    parmGroup.addParmTemplate(addSrcParm)
    node.setParmTemplateGroup(parmGroup)

    node.parm('file').set(path)
    node.parm('version').set("v`padzero(3,opdigits('.'))`")
    node.parm('source').set(f'../{node_name}')

    return node


def run(n):

    if n.type().nameComponents()[2]=='nmFileCache':

        n_name = n.name()
        n_pos = n.position()
        n_parent = n.parent()
        validRange = n.parm('trange').eval()
        is_wedge = n.parm('wedgeSwitch').eval() == 1

        sPath = "$HIP/../cache/Geometry/`chs((chsop('source')+'/safetyDir'))`/`chs('version')`/`opname(chs('source'))`_`chs('version')`"
        wPath = "$HIP/../cache/Wedge/`chs((chsop('source')+'/safetyDir'))`/`chs('version')`/`opname(chs('source'))`_`chs('version')`.w$SLICE"

        ver = 'v001'
        ext = n.parm('path_extension').evalAsString()

        
        
        parmnum = [0]

        if not is_wedge:
            ver = n.parm('version').eval()
            parmnum[0] += 1
            if validRange:
                sPath += '.$FF' + ext
            else:
                sPath += ext
            
            create_read_node(n_parent, n_name, ver, n_pos, sPath, is_wedge, parmnum)

        else:
            ver = n.parm('wedgeVersion').eval()
            if validRange:
                wPath += '.$FF' + ext
            else:
                wPath += ext

            create_read_node(n_parent, n_name, ver, n_pos, wPath, is_wedge, parmnum)



        



        
        



# def run(n):

#     if n.type().nameComponents()[2]=='nmCacheFile':
            
#         n_name = n.name()
#         n_pos = n.position()

#         validRange = n.parm('trange').eval()
#         sPath = "$HIP/../cache/Geometry/`chs((chsop('source')+'/safetyDir'))`/`chs('version')`/`opname(chs('source'))`_`chs('version')`"
#         wPath = "$HIP/../cache/Wedge/`chs((chsop('source')+'/safetyDir'))`/`chs('version')`/`opname(chs('source'))`_`chs('version')`.w$SLICE"

#         ver = 'v001'
#         ext = n.parm('path_extension').evalAsString()

#         addVerParm = eval('hou.%sParmTemplate("%s", "%s", 1,default_value=(["%s"]))' % ('String', 'version', 'Version ', 'v001'))
#         addSrcParm = hou.StringParmTemplate("source", "Source", 1, string_type=hou.stringParmType.NodeReference)
        
#         parmnum = [0]

#         if n.parm('wedgeSwitch').eval()==0:
#             ver = n.parm('version').eval()
#             parmnum[0] += 1
#             if validRange:
#                 sPath += '.$FF' + ext
#             else:
#                 sPath += ext

#             readS = n.parent().createNode('file','file__{}_{}'.format(n_name,ver))
#             readS.setPosition(n_pos+hou.Vector2(2,-1))
            
#             parm = readS.parms()[parmnum[0]]
#             parmTmp = parm.parmTemplate()
#             parmGroup = readS.parmTemplateGroup()
#             parmIndex = parmGroup.findIndices(parmTmp.name())[0]
#             parmGroup.insertAfter(parmGroup.parmTemplates()[parmIndex],addVerParm)
#             parmGroup.addParmTemplate(addSrcParm)
#             readS.setParmTemplateGroup(parmGroup)

#             readS.parm('file').set(sPath)
#             readS.parm('version').set("v`padzero(3,opdigits('.'))`")
#             readS.parm('source').set('../{}'.format(n_name))


#         else:
#             ver = n.parm('wedgeVersion').eval()
#             if validRange:
#                 wPath += '.$FF' + ext
#             else:
#                 wPath += ext

#             readW = n.parent().createNode('nmFileMerge','filemerge__{}_{}'.format(n_name,ver))
#             readW.setPosition(n_pos+hou.Vector2(2,-1))
            
#             parm = readW.parms()[parmnum[0]]
#             parmTmp = parm.parmTemplate()
#             parmGroup = readW.parmTemplateGroup()
#             parmIndex = parmGroup.findIndices(parmTmp.name())[0]
#             parmGroup.insertAfter(parmGroup.parmTemplates()[parmIndex],addVerParm)
#             parmGroup.addParmTemplate(addSrcParm)
#             readW.setParmTemplateGroup(parmGroup)

#             readW.parm('file').set(wPath)
#             readW.parm('version').set("v`padzero(3,opdigits('.'))`")
#             readW.parm('source').set('../{}'.format(n_name))
                     

        



        
        