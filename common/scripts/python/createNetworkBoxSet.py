import hou
import os
import json

def run():
    user_json = get_user_json_path()

    if os.path.exists(user_json):
        json_open = open(user_json, 'r')
        netBoxLists = json.load(json_open)

    else:
        netBoxLists = {
                "Camera": {
                    "color": [0.1,0.1, 0.1], 
                    "name": "nm_Camera", 
                    "pos": [ 5.0, 0.0], 
                    "size": [20.0, 2.0]
                }, 
                "Import-Chr": {
                    "color": [0.62, 0.77, 0.87], 
                    "name": "nm_Import-Chr", 
                    "pos": [5.0, -12.0], 
                    "size": [20.0, 4.0]
                }, 
                "Import-Prop": {
                    "color": [0.77,      0.77,    0.87], 
                    "name": "nm_Import-Prop", 
                    "pos": [5.0, -16.0], 
                    "size": [20.0, 3.0]
                }, 
                "Import-Stage": {
                    "color": [0.62,      0.87,    0.77], 
                    "name": "nm_Import-Stage", 
                    "pos": [5.0, -7.0], 
                    "size": [20.0, 3.0]
                }, 
                "Light": {
                    "color": [1.0, 0.98, 0.67], 
                    "name": "nm_Light", 
                    "pos": [5.0, -3.0], 
                    "size": [20.0, 2.0]
                }, 
                "Render": {
                    "color": [0.57, 0.49, 0.86], 
                    "name": "nm_Render", 
                    "pos": [5.0, -31.0], 
                    "size": [20.0, 6.0]
                }, 
                "Shader": {
                    "color": [0.99, 0.65, 0.65], 
                    "name": "nm_Shader", 
                    "pos": [5.0, -24.0], 
                    "size": [20.0, 2.0]
                }, 
                "Work": {
                    "color": [0.56, 0.1, 0.1], 
                    "name": "nm_Work", 
                    "pos": [ 5.0, -21.0], 
                    "size": [ 20.0, 4.0 ]
                }
            }
    
    obj = hou.node('/obj')

    for nName,nAttr in netBoxLists.items():
        box = obj.createNetworkBox()
        box.setComment(nName)
        box.setName(nAttr['name'])
        box.setPosition(hou.Vector2(nAttr['pos']))
        box.setColor(hou.Color(nAttr['color']))
        box.setSize(hou.Vector2(nAttr['size']))
      

def get_user_json_path():
    py_file = __file__
    py_dir  = os.path.dirname(py_file)
    user_json = os.path.join(py_dir, 'createNetworkBoxSet_userSetting.json')

    return user_json
    

def user_orginal_write(user_json=get_user_json_path()):

    if os.path.exists(user_json):
        choose = hou.ui.displayMessage(
                        "This file is already existing. Are you want to overwrite? \n{}".format(user_json), 
                        buttons=("Overwrite",'Cancel'), 
                        severity=hou.severityType.Message, 
                        title="[Nagamochi][CreateNetworkBox] Save User Preset"
                        )
        if choose==1:
            return None

    sels = hou.selectedItems()
    netBoxList = {}
    round_num = 3 

    for sel in sels:
        options = {}
        options['name'] = sel.name()
        options['pos'] = [round(n, round_num) for n in list(sel.position())] 
        options['size'] = [round(n, round_num) for n in list(sel.size())] 
        options['color'] = [round(n, round_num) for n in list(sel.color().rgb())] 
        netBoxList[sel.comment()] = options   

    with open(user_json, 'w') as f:
        json.dump(netBoxList, f, ensure_ascii=False, sort_keys=True,indent=4)

