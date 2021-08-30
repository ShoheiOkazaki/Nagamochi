import hou
import doppyrotoolutils
import defaulttools
import dopsmoketoolutils
import toolutils


# get size of selectednode
def getSize(selectedobject):
        (invis, bbox) = defaulttools.calculateBoundingBox(selectedobject, None, True)
        diam = bbox.sizevec()[0] + bbox.sizevec()[1] + bbox.sizevec()[2]
        diam = diam / 3.

        op_mult = diam / 2.0
        return op_mult

def op_mult(val, diam):
    """ Multiplies val by diam
    """
    return val * diam


def billowySmoke(n, creatednodes, clustering=False):
    diam = getSize(n)
    divdiam = diam / 2.0
    #op_mult = diam

    for creatednode in creatednodes:
        if creatednode.type().nameComponents()[2].lower().find('pyrosource') != -1:
            fluidsource = creatednode
    # fluidsource = toolutils.findOutputNodeOfType(n,'pyrosource')

    featheramount = 0.125
    if fluidsource != None:
                    doppyrotoolutils.applyParmSet(fluidsource, divdiam,
                                                                    [
                                                                    ('scale1',1.2,None),
                                                                    ('scale2',1.2,None),
                                                                    ('particlesep',featheramount,op_mult)
                                                                    ])
                    noisenode = toolutils.findOutputNodeOfType(fluidsource, 'attribnoise')
                    if noisenode != None:
                            doppyrotoolutils.applyParmSet(noisenode, diam,
                                    [
                                    ('outmin1', -1.2, None),
                                    ('outmax1', 1.2, None),
                                    ('attribs', fluidsource.parm('name1').evalAsString() + " " + fluidsource.parm('name2').evalAsString(), None),
                                    ('elementsize', 1, op_mult),
                                    ('pulseduration', 5, None),
                                    ('remap', True, None),
                                    ('clampmin', True, None)
                                    ])
                            doppyrotoolutils.buildRamp(noisenode, 'pdf', 'monotonecubic',
                                            [
                                            (0, 1),
                                            (0.2, 0.7),
                                            (0.4, 0.3),
                                            (0.6, 0.1),
                                            (0.8, 0.05),
                                            (1, 0)
                                            ])
                    noisenode2 = toolutils.findOutputNodeOfType(fluidsource, 'attribnoise::2.0')
                    if noisenode2 != None:
                            doppyrotoolutils.applyParmSet(noisenode2, diam,
                                    [
                                    ('attribtype','float',None),
                                    ('amplitude', 2.0, None),
                                    ('attribs', fluidsource.parm('name1').evalAsString() + " " + fluidsource.parm('name2').evalAsString(), None),
                                    ('outputraw', False, None),
                                    ('elementsize', 1, op_mult),
                                    ('pulseduration', 5, None),
                                    ('enableremap', True, None),
                                    ('doclampmin', True, None)
                                    ])
                            doppyrotoolutils.buildRamp(noisenode2, 'remapramp', 'monotonecubic',
                                            [
                                            (0, 0),
                                            (0.2, 0.05),
                                            (0.4, 0.1),
                                            (0.6, 0.3),
                                            (0.8, 0.7),
                                            (1, 1)
                                            ])


def burn(fuelgeo,creatednodes, clustering=False):
    diam = getSize(fuelgeo)
    divdiam = diam / 2.0
    #op_mult = diam 

    #fluidsource = toolutils.findOutputNodeOfType(fuelgeo,'pyrosource')
    for creatednode in creatednodes:
        if creatednode.type().nameComponents()[2].lower().find('pyrosource') != -1:
            fluidsource = creatednode
    featheramount = 0.1
    if fluidsource != None:
                doppyrotoolutils.applyParmSet(fluidsource, divdiam,
                                         [
                                         ('scale1',1.9,None),
                                         ('scale2',1.9,None),
                                         ('particlesep',featheramount,op_mult)
                                         ])
                noisenode = toolutils.findOutputNodeOfType(fluidsource, 'attribnoise')
                if noisenode != None:
                    doppyrotoolutils.applyParmSet(noisenode, diam,
                        [
                        ('outmin1', -1.9, None),
                        ('outmax1', 1.9, None),
                        ('attribs', fluidsource.parm('name1').evalAsString() + " " + fluidsource.parm('name2').evalAsString(), None),
                        ('elementsize', 1, op_mult),
                        ('remap', True, None),
                        ('clampmin', True, None)
                        ])
                    doppyrotoolutils.buildRamp(noisenode, 'pdf', 'monotonecubic',
                            [
                            (0, 1),
                            (0.2, 0.7),
                            (0.4, 0.3),
                            (0.6, 0.1),
                            (0.8, 0.05),
                            (1, 0)
                            ])

def addpointvel(n,creatednodes,usevel=True):
    parent = n.parent()
    raster = toolutils.findOutputNodeOfType(n,'volumerasterizeattributes')
    inn = raster.inputs()[0]

    velocity = parent.createNode("pointvelocity")#, "get_velocity")
    if usevel:
        velocity.parm("init").set(1)
    velocity.parm("addobjectmotion").set(False)
    velocity.parm("objpath").set("`opfullpath('..')`")
    
    velocity.setInput(0,inn)
    raster.insertInput(0,velocity)
    
    visType =  hou.viewportVisualizers.types()[0]
    vis = hou.viewportVisualizers.createVisualizer(visType,category=hou.viewportVisualizerCategory.Node,node=velocity)
    vis.setIsActive(1, viewport=None)
    vis.setName('source_velocity')
    vis.setParm('style','vector')
    vis.setParm('attrib','v')
    vis.setParm('unitlength',hou.fps())
    
    creatednodes.insert(2,velocity)
    return velocity,creatednodes
    
def addfluidsource(objecttoconvert, preset, mode, volumeattribute, addnoise=False):
    # These presets cause creation of a pyro source (the rest get FLIP source).
    pyropresets = ["source", "sourcefuel"]
    usepyrosource = (preset in pyropresets)

    # The list of all created nodes by this function.
    creatednodes = []

    parent = objecttoconvert.parent()

    if len(volumeattribute) == 0:
        name = "create_Vel"
    else:
        name = "create_%s" % volumeattribute

    # Create the appropriate source SOP.
    if usepyrosource:
        try:
            newfluidsource = parent.createNode("nmPyroSource", name)
        except:
            newfluidsource = parent.createNode("pyrosource", name)
    else:
        newfluidsource = parent.createNode("flipsource", name)
    creatednodes.append(newfluidsource)

    newfluidsource.hdaModule().set(newfluidsource.path(), preset)
    if usepyrosource and mode != "Auto":
        newfluidsource.parm("mode").set(mode)
    newfluidsource.setInput(0, objecttoconvert)

    # If trying to source from volume into a flip source, make sourcing volumetric.
    if not usepyrosource and mode == 2:
        newfluidsource.parm("shell").set(False)

    # Create a noise node if we're sourcing pyro.
    noisenode = None
    if usepyrosource and addnoise:
        noisenode = parent.createNode("attribnoise", "add_noise")

        if noisenode.type().nameComponents()[-1]!='2.0':
            noisenode.parm("signature").set("dim1")
        else:
            noisenode.parm("operation").set("set")

        noisenode.parm("animated").set(True)
        noisenode.parm("fractal").set("none")
        noisenode.setInput(0, newfluidsource)
        creatednodes.append(noisenode)
        inputnode = noisenode
    else:
        inputnode = newfluidsource

    # Add the rasterization node for pyro sourcing.
    rasterizer = None
    if usepyrosource:
        rasterizer = parent.createNode("volumerasterizeattributes", "rasterize")
        rasterizer.parm("points").set("particles")
        rasterizer.parm("attributes").set("density temperature fuel Cd Alpha v")
        rasterizer.parm("voxelsize").setExpression('ch("%s") * ch("%s") / 4' %
            (newfluidsource.parm("particlesep").path(), newfluidsource.parm("particlescale").path()))
        rasterizer.parm("densityattrib").set("")
        rasterizer.parm("normalize").set(True)
        rasterizer.setInput(0, inputnode)
        creatednodes.append(rasterizer)
        inputnode = rasterizer

    return inputnode, creatednodes


#selectedobject = hou.node('/obj/torus_object1/__in')


def run(selectedobject,simtype='billowySmoke'):
    parent = selectedobject.parent()
    has_v = dopsmoketoolutils.haspointattribute(selectedobject)
    convertmode = doppyrotoolutils.incominggeotype(selectedobject)

    # return preset name and sampleattribute
    #preset = convertlist[1]
    #sampleattribute = convertlist[0]

    # make sure data is there to run sourcing operation on
    geopresent = dopsmoketoolutils.count(selectedobject, convertmode)

    # If we're sourcing from volumes and no volumes are actually present, try to source from
    # the surface.
    originalconvertmode = convertmode
    usevolume = False
    if geopresent == 0 and convertmode == 'Volume':
        convertmode = 'Surface'
        geopresent = dopsmoketoolutils.count(selectedobject, convertmode)
        usevolume = True

    if convertmode == "Surface" or convertmode == "Points":
        if convertmode == "Points":
            convertmode = 1
        elif usevolume:
            convertmode = 2
        else:
            convertmode = 0


    # create nodes for convert to vol
    if simtype == 'billowySmoke':
        inputnode, creatednodes =addfluidsource(selectedobject, 'source', convertmode, 'density', addnoise=True)

    elif simtype == 'burn':
        inputnode, creatednodes =addfluidsource(selectedobject, 'sourcefuel', convertmode, 'burn', addnoise=True)
    


    if has_v:
        (velocity,creatednodes) = addpointvel(selectedobject,creatednodes,usevel=True)
    else:
        (velocity,creatednodes) = addpointvel(selectedobject,creatednodes,usevel=False)
            
    
    # set parms
    if simtype == 'billowySmoke':
        billowySmoke(selectedobject,creatednodes)

    if simtype == 'burn':
        burn(selectedobject,creatednodes)

    n_pyroSrc = None
    n_raster = None
    # move nodes in list to good position
    for node in creatednodes:
        node.moveToGoodPosition()
        if node.type().name() == 'pyrosource':
            n_pyroSrc = node    
        elif node.type().name() == 'volumerasterizeattributes':
            n_raster = node 
    if n_raster != None and n_pyroSrc != None:
        p_voxelsize = n_raster.parm('voxelsize').expression()
        r_path = n_raster.relativePathTo(n_pyroSrc)
        p_voxelsize = p_voxelsize.replace(n_pyroSrc.path(),r_path)
        n_raster.parm('voxelsize').setExpression(p_voxelsize)

#print has_v,inputnode
