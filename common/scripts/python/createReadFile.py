import hou
import os
#n = hou.selectedNodes()[0]
#n = hou.node('/obj/work_fire/sim_fire_base')


def run(n):

    if n.type().nameComponents()[2]=='nmCacheFile':
            
        n_name = n.name()
        n_pos = n.position()

        validRange = n.parm('trange').eval()
        sPath = "$HIP/../cache/Geometry/`chs((chsop('source')+'/safetyDir'))`/`chs('version')`/`opname(chs('source'))`_`chs('version')`"
        wPath = "$HIP/../cache/Wedge/`chs((chsop('source')+'/safetyDir'))`/`chs('version')`/`opname(chs('source'))`_`chs('version')`.w$SLICE"

        ver = 'v001'
        ext = n.parm('path_extension').evalAsString()

        addVerParm = eval('hou.%sParmTemplate("%s", "%s", 1,default_value=(["%s"]))' % ('String', 'version', 'Version ', 'v001'))
        addSrcParm = hou.StringParmTemplate("source", "Source", 1, string_type=hou.stringParmType.NodeReference)
        
        parmnum = [0]

        if n.parm('wedgeSwitch').eval()==0:
            ver = n.parm('version').eval()
            parmnum[0] += 1
            if validRange:
                sPath += '.$FF' + ext
            else:
                sPath += ext

            readS = n.parent().createNode('file','file__{}_{}'.format(n_name,ver))
            readS.setPosition(n_pos+hou.Vector2(2,-1))
            
            parm = readS.parms()[parmnum[0]]
            parmTmp = parm.parmTemplate()
            parmGroup = readS.parmTemplateGroup()
            parmIndex = parmGroup.findIndices(parmTmp.name())[0]
            parmGroup.insertAfter(parmGroup.parmTemplates()[parmIndex],addVerParm)
            parmGroup.addParmTemplate(addSrcParm)
            readS.setParmTemplateGroup(parmGroup)

            readS.parm('file').set(sPath)
            readS.parm('version').set("v`padzero(3,opdigits('.'))`")
            readS.parm('source').set('../{}'.format(n_name))


        else:
            ver = n.parm('wedgeVersion').eval()
            if validRange:
                wPath += '.$FF' + ext
            else:
                wPath += ext

            readW = n.parent().createNode('nmFileMerge','filemerge__{}_{}'.format(n_name,ver))
            readW.setPosition(n_pos+hou.Vector2(2,-1))
            
            parm = readW.parms()[parmnum[0]]
            parmTmp = parm.parmTemplate()
            parmGroup = readW.parmTemplateGroup()
            parmIndex = parmGroup.findIndices(parmTmp.name())[0]
            parmGroup.insertAfter(parmGroup.parmTemplates()[parmIndex],addVerParm)
            parmGroup.addParmTemplate(addSrcParm)
            readW.setParmTemplateGroup(parmGroup)

            readW.parm('file').set(wPath)
            readW.parm('version').set("v`padzero(3,opdigits('.'))`")
            readW.parm('source').set('../{}'.format(n_name))
                     

        



        
        