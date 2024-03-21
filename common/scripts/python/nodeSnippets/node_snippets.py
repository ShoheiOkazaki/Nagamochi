import hou

def add_spare_input(kwargs):
    node = kwargs["node"]

    spare_num = 0
    spare_find = True
    while spare_find:
        if node.parm(f'spare_input{spare_num}'):
            spare_num +=1        
        else:
            spare_find = False

    spare_node = None
    for sel in hou.selectedNodes():
        if sel != node:
            spare_node = sel

    ptg = node.parmTemplateGroup()
    ptg.append(hou.StringParmTemplate(f'spare_input{spare_num}', f'Spare Input {spare_num}', 1,string_type = hou.stringParmType.NodeReference))
    node.setParmTemplateGroup(ptg)
    node.parm(f'spare_input{spare_num}').set(node.relativePathTo(spare_node))