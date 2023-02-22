import hou
import os, re, time

from nagamochi_utils import MSG
script_name = 'IncrementalSave'


def get_available_path(hip_full_path, increment='major', add_minor=True):
    pattern=r'([0-9]*)'

    hipfile = os.path.splitext(os.path.basename(hip_full_path))[0] 
    versionType, version_sepalotor, versionMajor, versionMinor = get_curent_version(hipfile)

    if increment == 'major':
        edit_target_majver = versionMajor
        majver_match = re.findall(pattern,edit_target_majver)
        if majver_match:
            versionNumber = majver_match[-2]
            new_majver = str(int(versionNumber) + 1).zfill(len(versionNumber))
            new_minver = str(int(1)).zfill(len(versionMinor))

    else:
        new_majver = versionMajor
        if len(versionMinor):
            edit_target_minver = versionMinor
            minver_match = re.findall(pattern,edit_target_minver)
            if minver_match:
                versionNumber = minver_match[-2]                
                new_minver = str(int(versionNumber) + 1).zfill(len(versionNumber))        

    # else:
    #     message_w =  "[Nagamochi] Problem encountered matching version number - Exiting"
    #     #rint message_w
    #     hou.ui.setStatusMessage(message_w)
    #     exit()

    old_majver_str = '{}{}'.format(versionType,versionMajor)
    new_majver_str = '{}{}'.format(versionType,new_majver)    

    if len(versionMinor):
        newhip = hip_full_path.replace(old_majver_str, new_majver_str)
        new_minver_str = '{}{}'.format(version_sepalotor,new_minver)  
        newhip = newhip.replace('{}{}'.format(version_sepalotor,versionMinor), new_minver_str)
    else:
        if add_minor:
            newhip = hip_full_path.replace(old_majver_str, new_majver_str + '.001')
        else:
            newhip = hip_full_path.replace(old_majver_str, new_majver_str)

    return newhip


def get_curent_version(hipfile):
    versionSections = ""
    versionType = ""
    version_sepalotor = '' 
    versionMinor = ''

    if len(re.findall('_v(?=\d+)', hipfile)) > 0:
        versionSections = re.split('_v(?=\d+)', hipfile, 1)        
        versionType = "_v"
    elif len(re.findall('_V(?=\d+)', hipfile)) > 0:
        versionSections = re.split('_V(?=\d+)', hipfile, 1)          
        versionType = "_V"
    elif len(re.findall('.v(?=\d+)', hipfile)) > 0:
        versionSections = re.split('.v(?=\d+)', hipfile, 1)        
        versionType = ".v"
        
    # find Minor version
    find_seps = re.findall('\\.|_', versionSections[1])      

    if len(find_seps)==1:
        version_sepalotor = find_seps[0]        
        versionMajor = versionSections[1].split(version_sepalotor)[0]
        versionMinor = versionSections[1].split(version_sepalotor)[1]
    else:
        versionMajor = versionSections[1]

    return versionType, version_sepalotor, versionMajor, versionMinor


def run():
    # ======== Get current info ========
    hip_full_path = hou.hipFile.name()
    hipname = hou.hipFile.basename()
    hipfile = os.path.splitext(hipname)[0]
    #print(hip_full_path,hipname,hipfile)

    has_minor = False
    versionType, version_sepalotor, versionMajor, versionMinor = get_curent_version(hipfile)
    #print(versionType, versionMajor,versionMinor)

    # ======== User Choice ========    
    ui_botton = ("Major Up","Minor Up",'Cancel')
    ui_text = hipname
    ui_text += '\n\nMajor: {}'.format(versionMajor)    

    if(len(versionMinor)):
        has_minor = True
        ui_text += '\nMinor: {}'.format(versionMinor)
        
    choose = hou.ui.displayMessage(
                ui_text, 
                buttons = ui_botton, 
                severity = hou.severityType.Message, 
                title = "[Nagamochi] Incremental Save"
            )

    targetVer = ''

    if choose==0:
        new_ver_path = get_available_path(hip_full_path, increment='major', add_minor=False)

    elif choose==1:
        new_ver_path = get_available_path(hip_full_path, increment='minor')

    else:
        #print 'cancel'
        #return 0
        exit()
        
    #checkEnv = hou.getenv('MAJVER') and hou.getenv('MINVER')
    # print(new_ver_path)

    # ======== Save the file ======== 
    confirm = 0
    if os.path.isfile(new_ver_path) :
        text = "Overwrite the existing hip file?"
        confirm = hou.ui.displayMessage(text, buttons=("Yes", "No"), severity=hou.severityType.Message, title="Save New Hip Version")
    if confirm == 0 :
        hou.hipFile.save(new_ver_path)
        save_time = time.ctime(os.path.getmtime(new_ver_path))

        message = '[Nagamochi] Successfully saved %s (%s)' % (hou.hipFile.basename(),save_time)

        hou.ui.setStatusMessage(message)
