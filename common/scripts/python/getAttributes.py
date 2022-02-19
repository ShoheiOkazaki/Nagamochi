import hou
#N = hou.node('/obj/work_windImpactA/blast7')
import itertools

def attribLabel(a):
    had=hou.attribData
    td = { had.String:'s', had.Int:'i', had.Float:'f' }
    t = a.dataType()
    ts = a.size()
    ty = '?'
    if t in td: 
        ty = td[t]
    if ts==3: 
        ty='v'
    if ts==4: 
        ty='p'
    #pq = ptAttr.qualifier()
    #if pq=='': pq=' '
    attr_q = a.qualifier()
    if len(attr_q):
        attr_q = ' ({})'.format(attr_q)
    label = "{}@{}{}".format( ty, a.name(), attr_q )
    return str(label)
    
    
def getPointAttrs(N):
    attrs_pt = []
    if N.geometry() is not None:
        for pt in N.geometry().pointAttribs():
            attrs_pt.append( pt.name() )
    return attrs_pt

def getPrimAttrs(N):
    attrs_pr = []
    if N.geometry() is not None:
        for pr in N.geometry().primAttribs():
            attrs_pr.append( pr.name() )
    return attrs_pr

def getVertexAttrs(N):
    attrs_vx = []
    if N.geometry() is not None:        
        for vx in N.geometry().vertexAttribs():
            attrs_vx.append( vx.name() )
    return attrs_vx

def getDetailAttrs(N):
    attrs_de = []
    if N.geometry() is not None:
        for de in N.geometry().globalAttribs():
            attrs_de.append( de.name() )
    return attrs_de

def getIntrinsics(N):
    attrs_in = []
    if N.geometry() is not None:
        for intr in N.geometry().prims()[0].intrinsicNames():
            attrs_in.append( intr )
    return attrs_in


def buildList(N,inPt=True,inPr=True,inVx=True,inDe=True,inIntrinsics=False,addAttrType=False):
    
    attrs = []

    if N.inputs():

        attrs_pt = []
        attrs_pr = []
        attrs_vx = []
        attrs_de = []

        if inPt: 
            attrs_pt = getPointAttrs(N)            
        if inPr:
            attrs_pr = getPrimAttrs(N)
        if inVx:
            attrs_vx = getVertexAttrs(N)
        if inDe:
            attrs_de = getDetailAttrs(N)

        if len(attrs_pt)>0 and inPt:
            attrs += [None,'-----Points-----']
            attrs_pt.sort()
            attrs_pt_l = [attribLabel(N.geometry().findPointAttrib(pt)) for pt in attrs_pt]
            if addAttrType:
                attrs_pt = list(itertools.zip_longest(attrs_pt,[],fillvalue='point'))
            attrs += sum(zip(attrs_pt, attrs_pt_l),())
        if len(attrs_pr)>0 and inPr:
            attrs += [None,'-----Primitives-----']
            attrs_pr.sort()
            attrs_pr_l = [attribLabel(N.geometry().findPrimAttrib(pr)) for pr in attrs_pr]
            if addAttrType:
                attrs_pr = list(itertools.zip_longest(attrs_pr,[],fillvalue='prim'))
            attrs += sum(zip(attrs_pr, attrs_pr_l),())
        if len(attrs_vx)>0 and inVx:
            attrs += [None,'-----Vertices-----']
            attrs_vx.sort()
            attrs_vx_l = [attribLabel(N.geometry().findVertexAttrib(vx)) for vx in attrs_vx]
            if addAttrType:
                attrs_vx = list(itertools.zip_longest(attrs_vx,[],fillvalue='ver'))
            attrs += sum(zip(attrs_vx, attrs_vx_l),())
        if len(attrs_de)>0 and inDe:
            attrs += [None,'-----Detail-----']
            attrs_de.sort()
            attrs_de_l = [attribLabel(N.geometry().findGlobalAttrib(de)) for de in attrs_de]
            if addAttrType:
                attrs_de = list(itertools.zip_longest(attrs_de,[],fillvalue='guess'))
            attrs += sum(zip(attrs_de, attrs_de_l),())

    return attrs

#print(getIntrinsics(N))