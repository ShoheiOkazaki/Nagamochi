import hou
import os, re, time

def run():
    # ======== Get current info ========
    orighip = hou.hipFile.name()
    hipname = hou.hipFile.basename()
    hipfile = os.path.splitext(hipname)[0]

    #print orighip,'\n',hipname,'\n',hipfile,'\n'

    versionSections = ""
    versionType = ""
    if len(re.findall('_v(?=\d+)', hipfile)) > 0:
        versionSections = re.split('_v(?=\d+)', hipfile, 1)        
        versionType = "_v"
    elif len(re.findall('_V(?=\d+)', hipfile)) > 0:
        versionSections = re.split('_V(?=\d+)', hipfile, 1)          
        versionType = "_V"
    elif len(re.findall('.v(?=\d+)', hipfile)) > 0:
        versionSections = re.split('.v(?=\d+)', hipfile, 1)        
        versionType = ".v"
        
    versionMajor   = versionType + versionSections[1]
    # versionMajor = versionSections[1].split('_')[0]
    # versionMinor = versionSections[1].split('_')[1]

    #print versionMajor,versionMinor,len(versionMajor),'\n'


    # ======== create new version ========

    # regex - match numbers after version splitter. Match until non-numeric value is hit.
    targetVer = ''

    text = 'Current Version:\n %s ' % versionMajor.replace('_','').replace('.','')
    choose = hou.ui.displayMessage(text, buttons=("Incremental Save",'Cancel'), severity=hou.severityType.Message, title="Save New Hip Version")

    if choose==0:
        targetVer = versionMajor
    else:
        #print 'cancel'
        #return 0
        exit()
        
    pattern=r'([0-9]*)'
    match = re.findall(pattern,targetVer)

    if match:
        versionNumber = match[-2]
    else:
        message_w =  "[Nagamochi] Problem encountered matching version number - Exiting"
        #rint message_w
        hou.ui.setStatusMessage(message_w)
        exit()

    newVersion = str(int(versionNumber) + 1).zfill(len(versionNumber))
        
    #print versionNumber,'->',newVersion

    # ==== Set Var ====
    # seceneinfos = hipfile.split('_')
    # get_seq  = seceneinfos[0]
    # get_shot = seceneinfos[1]
    # get_proj = seceneinfos[2]
    # get_vari = seceneinfos[3]

    #print seceneinfos

    #checkEnv = hou.getenv('MAJVER') and hou.getenv('MINVER')
    newVersionStr = ''
    if choose==0:
        newVersionStr = '%s%s' % (versionType,newVersion)
    #     # if checkEnv:
    #     hou.hscript("setenv FX_VER=\'{}\'".format(newVersion))
    #     hou.hscript("setenv FX_SEQ=\'{}\'".format(get_seq))
    #     hou.hscript("setenv FX_SHOT=\'{}\'".format(get_shot))
    #     hou.hscript("setenv FX_PROJ=\'{}\'".format(get_proj))
    #     hou.hscript("setenv FX_VARI=\'{}\'".format(get_vari))
                

    newhip = orighip.replace(versionMajor, newVersionStr)

    # ======== Save the file ======== 
    confirm = 0
    if os.path.isfile(newhip) :
        text = "Overwrite the existing hip file?"
        confirm = hou.ui.displayMessage(text, buttons=("Yes", "No"), severity=hou.severityType.Message, title="Save New Hip Version")
    if confirm == 0 :
        hou.hipFile.save(newhip)
        save_time = time.ctime(os.path.getmtime(newhip))
        
        message = '[Nagamochi] Successfully saved %s (%s)' % (hou.hipFile.basename(),save_time)
        
        hou.ui.setStatusMessage(message)
        
    #print newhip
    #print '----------------------------------\n'