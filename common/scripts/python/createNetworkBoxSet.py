import hou

def run():
  netBoxLists = {
             #-name-:[ ---Position---- ,  -----Size------ , -----------Color------------,]
            'Camera':[hou.Vector2(5,-0), hou.Vector2(20,2),hou.Color((0.10, 0.10, 0.10)),],
             'Light':[hou.Vector2(5,-3), hou.Vector2(20,2),hou.Color((1.00, 0.98, 0.67)),],
      'Import-Stage':[hou.Vector2(5,-7), hou.Vector2(20,3),hou.Color((0.62, 0.87, 0.77)),],
        'Import-Chr':[hou.Vector2(5,-12),hou.Vector2(20,4),hou.Color((0.62, 0.77, 0.87)),],
       'Import-Prop':[hou.Vector2(5,-16),hou.Vector2(20,3),hou.Color((0.77, 0.77, 0.87)),],
              'Work':[hou.Vector2(5,-21),hou.Vector2(20,4),hou.Color((0.56, 0.10, 0.10)),],
            'Shader':[hou.Vector2(5,-24),hou.Vector2(20,2),hou.Color((0.99, 0.65, 0.65)),],
            'Render':[hou.Vector2(5,-31),hou.Vector2(20,6),hou.Color((0.57, 0.49, 0.86)),],
            }

      
  obj = hou.node('/obj')

  for nName,nAttr in netBoxLists.items():
      box = obj.createNetworkBox()
      box.setComment(nName)
      box.setName('nm_{}'.format(nName))
      box.setPosition(nAttr[0])
      box.setColor(nAttr[2])
      box.setSize(nAttr[1])
      