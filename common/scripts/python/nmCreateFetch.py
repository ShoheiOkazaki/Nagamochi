import hou

def main(nodes):
    
    expectedNodes = ['nm File Cache']

    if len(nodes) > 0:
        for n in nodes:

            nodeType = n.type().description()

            if not nodeType in expectedNodes:
            	print("[nmCreateFetch] ==%s== is not unexpected node. Just brushed it off." % n.path())
            	pass
           
            else:
                nodeType = nodeType.replace(" ", "")
                nName = n.name()
                nColor = n.color()
                sourcePath = n.path() + "/To_Fetch"
                nodePath = []
                nodePath.append(n.path())
                jobTittle = []
                jobCom = ""
                ropType =  chooseRopType(nodeType,n.path())
                outputParm = str('`chs("' + nodePath[0] + '/file")`')
                #srcTrange = node.parm('trange').eval()
                
                if (ropType==3):
                    pass

                elif (ropType==0): #fetch
                    nName = "%s__%s" % (nodeType.replace('nm',''),n.name())
                    outRop = createFetch(nName,nColor,sourcePath)
                    n.parm('ropPath').set(outRop.path())
                    n.parm('wedgeSwitch').set(0)


                elif (ropType==1): #alembic or geometry
                    nName = "%s__%s" % (nodeType.replace('nm',''),n.name())
                    if "Abc" in nodeType:
                        outRop = createAlembic(nName,nColor,n.path())
                    else:
                        outRop = createGeometry(nName,nColor,n.path())
                    n.parm('ropPath').set(outRop.path())
                    n.parm('wedgeSwitch').set(0)

                elif (ropType==2): #wedge
                    nName = "%sWedge__%s" % (nodeType.replace('nm',''),n.name())
                    outRop = createWedge(nName,nColor,n.path())
                    n.setParms({
                        'ropPath'  : outRop.path(),
                        'wedgeSwitch' : 1,
                        })
                    if n.parm('WedgeFileMerge_mergerange1'):
                        n.setParmExpressions({
                            'WedgeFileMerge_mergerange1': "ch(chs('ropPath')/range1x)",
                            'WedgeFileMerge_mergerange2': "ch(chs('ropPath')/range1y)",
                            })




def chooseRopType(nodeType,nName):
    uiTitle = "Select Rop Type for %s" % (nName)
    if "Abc" in nodeType:
        choice2 = 'Alembic'
    else:
        choice2 = 'Geometry'
    uiMessage = "Which do you use for cahce?\n Target Node : [ %s ]" % (nName)
    ropTypeList = ['Fetch',choice2,'Wedge','Cancel']
    ropType = hou.ui.displayMessage(title=uiTitle, text=uiMessage, buttons=ropTypeList)
    return ropType


def createFetch(nName,nColor,sourcePath):
    # Create Fetch ROP and set Parm
    try:
        outRop = hou.node('/out').createNode('custom_Fetch', nName)
    except:
        outRop = hou.node('/out').createNode('fetch',nName)
    outRop.parm('source').set(sourcePath)        
    outRop.setColor(nColor)
    return outRop


def createAlembic(nName,nColor,sourcePath):
    outRop = hou.node('/out').createNode('alembic',nName)
    tpl = hou.StringParmTemplate("source", "Source", 1, string_type=hou.stringParmType.NodeReference)
    outRop.addSpareParmTuple(tpl)
    outRop.parm('f1').deleteAllKeyframes()
    outRop.parm('f2').deleteAllKeyframes()
    
    outRop.setParms({
        "use_sop_path" : 1,
        "source"  : sourcePath,
        "sop_path" : "`chs('source')`/TO_ROP",
            "filename" : "`chs(chsop('source')+'/filename')`",
        "path_attrib" : "_nmAbcPath",
        'full_bounds' : 1,
        'facesets' : 0,
        #"alfprogress" : 1,
        })
    outRop.setParmExpressions({
        "trange" : "ch(chs('source')+'/abc_type')",
        "f1" : "ch(chs('source')+'/f1')",
        "f2" : "ch(chs('source')+'/f2')",
        "f3" : "ch(chs('source')+'/f3')",
        "build_from_path" : "ch(chsop('source')+'/build_hier_from_path')",
        "facesets" :"ch(chsop('source')+'/facesets')",
        #"initsim" : "ch(chs('source')+'/initsim')",
        #"savebackground" : "ch(chs('source')+'/To_Fetch_savebackground')",
        })
    outRop.setColor(nColor)
    return outRop


def createGeometry(nName,nColor,sourcePath):
    outRop = hou.node('/out').createNode('geometry',nName)
    tpl = hou.StringParmTemplate("source", "Source", 1, string_type=hou.stringParmType.NodeReference)
    outRop.addSpareParmTuple(tpl)
    outRop.parm('f1').deleteAllKeyframes()
    outRop.parm('f2').deleteAllKeyframes()
    
    outRop.setColor(nColor)

    outRop.setParms({
        #"use_sop_path" : 1,
        "source"  : sourcePath ,
        "soppath" : "`chs('source')`/TO_ROP",
        "alfprogress" : 1,
        })
    outRop.setParmExpressions({
        "trange" : "ch(chs('source')+'/trange')",
        "f1" : "ch(chs('source')+'/f1')",
        "f2" : "ch(chs('source')+'/f2')",
        "f3" : "ch(chs('source')+'/f3')",
        "sopoutput" : "chs(chsop('source')+'/To_Fetch/sopoutput')",
        #"build_from_path" : "ch(chsop('source')+'/build_hier_from_path')"
        "initsim" : "ch(chs('source')+'/initsim')",
        "savebackground" : "ch(chs('source')+'/savebackground')",
        })
    if nName.startswith("Cache"):
        outRop.setParms({
            "prerender": "hou.node(hou.node('.').parm('source').eval()).hdaModule().pre_render( hou.node(hou.node('.').parm('source').eval()).path() )",
            "lprerender":"python",
            "postrender":"hou.node(hou.node('.').parm('source').eval()).hdaModule().post_render( hou.node(hou.node('.').parm('source').eval()).path() )",
            "lpostrender":"python",
            })
        outRop.setParmExpressions({
            "tpreframe": "ch(chs('source')+'/tpreframe')",
            "preframe": "chs(chs('source')+'/preframe')",
            "lpreframe": "ch(chs('source')+'/lpreframe')",
            "tpostframe": "ch(chs('source')+'/tpostframe')",
            "postframe": "chs(chs('source')+'/postframe')",
            "lpostframe": "ch(chs('source')+'/lpostframe')",
            "tpostwrite": "ch(chs('source')+'/tpostwrite')",
            "postwrite": "chs(chs('source')+'/postwrite')",
            "lpostwrite": "ch(chs('source')+'/lpostwrite')",
            })
    return outRop

def createWedge(nName,nColor,sourcePath):
    try:
        outRop = hou.node('/out').createNode('nmDeadlinePDGWedge',nName) 
        outRop.setParms({
            "source"  : sourcePath,
            "use_wedge_attr0" : 1,
            })                  
        outRop.setParmExpressions({
            "intrange0y" : 'ch("wedgecount0")-1',
            })


    except:
        outRop = hou.node('/out').createNode('wedge',nName)    
        tpl = hou.StringParmTemplate("source", "Source", 1, string_type=hou.stringParmType.NodeReference)
        outRop.addSpareParmTuple(tpl)

        outRop.setParms({
            "source"  : sourcePath,
            "prefix"  : "",
            "driver" : "`chs('source')`/To_Fetch",
            "wedgeparams" : 1,
            "random" : 0,
            })                  
        outRop.setParmExpressions({
            "range1y" : 'ch("steps1")-1',
            })
    outRop.setColor(nColor)
    return outRop

