import os
import hou
import ast
import fnmatch

def get_cam_paths():
    root = hou.node('/')
    cam_nodes = root.recursiveGlob('*', hou.nodeTypeFilter.ObjCamera)

    cam_paths = []

    for cam_node in cam_nodes:
        cam_paths.append(cam_node.path())
        
    return cam_paths


def return_list(list):
    return sum(zip(list, list),())


def getList(parms):
    menu_items = []
    if len(parms)==0:
        return menu_items

    parm = parms[0]
    parm_temp = parm.tuple().parmTemplate()
    parm_type = parm_temp.type().name()    
    node = parm.node().type().name()

    choiceImgPath = ['setImage','set image path']

    if parm_type=='String':
        # opinput
        if (parm_temp.stringType().name()=='NodeReference' or parm_temp.stringType().name()=='NodeReferenceList') and parm.name().startswith('cam')==False:
            menu_items = ["opinput00","opinputpath('.',0)","opinput10","opinputpath('..',0)"]
        
        # ifd and arnold
        elif node=='ifd' and parm_temp.stringType().name()=='FileReference' and parm.name().find('vm_cryptolayeroutput')!=-1:
            menu_items = ['setIfdCrypt','Set CryptoLayer']
        elif node=='ifd' and parm_temp.stringType().name()=='FileReference' and parm.name().find('vm_filename_plane')!=-1:
            menu_items = ['setIfdExtra','Set ExtraLayer']
        elif node=='ifd' and parm_temp.stringType().name()=='FileReference' and parm.name().find('vm_picture')!=-1:
            menu_items = choiceImgPath
        elif node=='arnold' and parm_temp.stringType().name()=='FileReference' and parm.name().find('ar_picture')!=-1:
            menu_items = choiceImgPath
        elif node=='arnold' and parm_temp.stringType().name()=='FileReference' and parm.name().find('ar_aov_separate_file')!=-1:
            menu_items = ['setArExtra','Set ExtraLayer']
        elif node=='opengl' and parm_temp.stringType().name()=='FileReference' and parm.name().find('picture')!=-1:
            menu_items = choiceImgPath
        elif node=='comp' and parm_temp.stringType().name()=='FileReference' and parm.name().find('copoutput')!=-1:
            menu_items = choiceImgPath


        # version
        elif  parm.name() == 'version_major':
            menu_items = ['v$FX_MAJVER','v$FX_MAJVER']
        elif  parm.name() == 'version_minor':
            menu_items = ['$FX_MINVER','$FX_MINVER']
        elif  parm.name().find('version')!=-1 or parm.name().find('wedgeVersion')!=-1:
            menu_items = ['v$FX_VER','v$FX_VER']    
        

        # set camera wiht var
        elif  parm.name().find('camera')!=-1 or parm.name().find('cam_campath')!=-1:
            menu_items = return_list(get_cam_paths())

        # point cloud
        elif  parm.name().find('pc_file')!=-1:
            menu_items = ['Set Path for Point Cloud','Set Path for Point Cloud']

        # group
        elif parm.name()=='group' or parm.name().startswith('snippet') or parm.name()=='bindgroup' or parm.name()=='parmname':
            import getAttributes
            #reload(getAttributes)
            inputs = parm.node().inputs()
            if node=='bind':
                inputs = parm.node().parent().inputs()
            if len(inputs)>0:
                menu_items =  getAttributes.buildList(inputs[0],addAttrType=True)
            #print menu_items


    if parm_type=='Float':
        if parm_temp.numComponents()==3:
            menu_items = [
                        "centerOwnVar","center own [ $CEX.. ]",  
                        "centerOwnExp","center own [ centroid(opinputpath('.',0),D_X).. ]",  
                        "centerUpExp","center up [ centroid(opinputpath('..',0),D_X).. ]",
                        "centerPickExp", "center pick [ centroid('../????',D_X).. ]",  
                        "bboxOwn","bbox own [ bbox(opinputpath('.',0),D_XSIZE)]",  
                        "bboxUp","bbox up [ bbox(opinputpath('..',0),D_XSIZE)]",
                        "bboxPick", "bbox pick [ bbox('../????',D_XSIZE).. ]", 
                        ]

    return menu_items



def setParms(parms,select):
    nameSchem = {('1','u'):'X', ('2','v'):'Y', ('3','w'):'Z'}

    pc_path = "$HIP/../cache/pc/$OS/`$OS`.$F4.pc"


    valDict_str = { "opinput00":"`opinputpath('.',0)`", 
                    "opinput10":"`opinputpath('..',0)`",
                    'v$FX_MAJVER':'v${FX_MAJVER}', 
                    '$FX_MINVER':'${FX_MINVER}',
                    'v$FX_VER':'v${FX_VER}',
                    'Set Path for Point Cloud':pc_path,
                    }

    valDict_float = {
                    "centerOwnVar":"$CEX", 
                    "centerOwnExp":"centroid(opinputpath('.',0),D_X)", 
                    "centerUpExp":"centroid(opinputpath('..',0),D_X)",
                    "centerPickExp":"centroid(====,D_X)", 
                    "bboxOwn":"bbox(opinputpath('.',0),D_XSIZE)", 
                    "bboxUp":"bbox(opinputpath('..',0),D_XSIZE)",
                    "bboxPick":"bbox(====,D_XSIZE)"
                    }

    if select in valDict_str.keys():
        parm = parms[0]
        parm.set(valDict_str[select])

        # make pc folder
        if select == 'Set Path for Point Cloud':
            pc_path_eval = parm.eval()
            pc_folder = os.path.dirname(pc_path_eval)
            if not os.path.exists(pc_folder):
                os.makedirs(pc_folder)


    elif select in valDict_float.keys():
        for parm in parms:
            parm_temp = parm.tuple().parmTemplate()
            if parm_temp.namingScheme().name()=='Base1':
                setvalue = valDict_float[select].replace('X',nameSchem[parm.name()[-1]])
            elif parm_temp.namingScheme().name()=='XYZW':
                setvalue = valDict_float[select].replace('X',parm.name()[-1].upper())
            parm.setExpression(setvalue)

    elif parms[0].name().find('camera')!=-1 or parms[0].name().find('cam_campath')!=-1:
        parms[0].set(select)

    elif parms[0].name()=='group' or parms[0].name().startswith('snippet') or parms[0].name()=='bindgroup'or parms[0].name()=='parmname':
        parm_value = ''
        if len(parms[0].eval()):
            parm_value = parms[0].eval() + ' '
        value_list = ast.literal_eval(select)
        # set value
        parms[0].set('{}@{}'.format(parm_value,value_list[0]))
        # set Group Type
        grptype_label = 'grouptype'
        targetnode = parms[0].node()
        nodeTemp = targetnode.parmTemplateGroup()
        if nodeTemp.find("bindgrouptype") is not None:
            grptype_label = 'bindgrouptype'

        if targetnode.parm(grptype_label):
            grplabels = targetnode.parm(grptype_label).menuItems()
            grpname_pattern = '{}*'.format(value_list[1])
            grp_match = fnmatch.filter(grplabels, grpname_pattern)[0]
            try:
                targetnode.parm(grptype_label).set(grp_match)
            except:
                pass


    elif select == "setIfdCrypt":
        parm = parms[0]
        node = parm.node()
        cryptLayer = parm.name().replace('vm_cryptolayeroutput','')
        cryptName  = "`chs('vm_cryptolayername{}')`".format(cryptLayer)
        mainOut = node.parm('vm_picture').unexpandedString()
        mainOuts = mainOut.split('.')
        #mainOuts[0] = "{}_{}".format(mainOuts[0],cryptName)
        #cryptOut = '.'.join(mainOuts)
        cryptOut = "{}/`chs('version')`/`chs('vm_cryptolayername'+opdigits($CH))`/`$OS`_`chs('vm_cryptolayername'+opdigits($CH))`.`chs('version')`.$F4.exr".format(mainOut.rsplit('/',2)[0])
        parm.set(cryptOut)

    elif select == "setIfdExtra":
        parm = parms[0]
        node = parm.node()
        extraLayer = parm.name().replace('vm_filename_plane','')
        extraName  = "`chs('vm_variable_plane{}')`".format(extraLayer)
        mainOut = node.parm('vm_picture').unexpandedString()
        #mainOuts = mainOut.split('.')
        # mainOuts[0] = "{}_{}".format(mainOuts[0],extraName)
        #mainOuts[-1] = "{}/{}".format(extraName,mainOuts[-1]).replace('`$OS`','`$OS`_{}'.format(extraName))
        #extraOut = '.'.join(mainOuts)
        extraOut = "{}/`chs('vm_variable_plane'+opdigits($CH))`/`$OS`_`chs('vm_variable_plane'+opdigits($CH))`.`chs('version')`.$F4.exr".format(mainOut.rsplit('/',2)[0])
        parm.set(extraOut)

    elif select == "setArExtra":
        parm = parms[0]
        node = parm.node()
        extraLayer = parm.name().replace('ar_aov_separate_file','').replace('_*','')
        extraName  = "`chs('ar_aov_label{}')`".format(extraLayer)
        mainOut = node.parm('ar_picture').unexpandedString()
        mainOuts = mainOut.split('/')
        # mainOuts[-1] = "{}/{}".format(extraName,mainOuts[-1]).replace('`$OS`','`$OS`_{}'.format(extraName))
        # extraOut = '/'.join(mainOuts)
        extraOut = "{}/`chs('ar_aov_label'+opdigits($CH))`/`$OS`_`chs('ar_aov_label'+opdigits($CH))`.`chs('version')`.$F4.exr".format(mainOut.rsplit('/',2)[0])
        parm.set(extraOut)

    elif select.startswith("setImag"):
        parm = parms[0]
        node = parm.node()
        
        parmImg = 'vm_picture'
        imgExt = 'exr'
        if node.type().name() == 'arnold':
            parmImg = 'ar_picture'
        elif node.type().name() == 'opengl':
            parmImg = 'picture'
            imgExt = 'jpg'
        elif node.type().name() == 'comp':
            parmImg = 'copoutput'
            imgExt = 'jpg'

        if select == 'setImage':
            coutpath = "$HIP/../render/`$OS`/`chs('version')`/`$OS`.`chs('version')`.$F4.{}".format(imgExt)
            node.parm(parmImg).deleteAllKeyframes()
            node.parm(parmImg).set(coutpath,language=None)
            # if node.parm('version'):
            #     node.parm('version').deleteAllKeyframes()
            #     node.parm('version').revertToDefaults()




