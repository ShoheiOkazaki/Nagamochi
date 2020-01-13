def check(parm):

    parm_temp = parm.tuple().parmTemplate()
    parm_type = parm_temp.type().name()
    if parm_type=='String':
        if parm_temp.stringType().name()=='NodeReference':
            return 1
        else:
            return 0
    else:
        return 0

def set(parm,target):
    sample = ["`opinputpath('.',0)`",]

    parm.set(sample[target])
    # import nodeSnippets.parm_Str_NodeRef as parm_Str_NodeRef
    # reload(parm_Str_NodeRef)
    # return parm_Str_NodeRef(kwargs["parms"][0])

def test(parm):
        print parm