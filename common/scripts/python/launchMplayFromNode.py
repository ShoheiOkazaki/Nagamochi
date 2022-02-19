import subprocess
import hou

def launch(switch):   

    n = hou.selectedNodes()[0]

    if switch == False:
        if n.type().name() == 'ifd':
            run_mplay(n,'vm_picture')        
        elif n.type().name() == 'opengl':
            run_mplay(n,'picture')
        elif n.type().name() == 'arnold':
            run_mplay(n,'ar_picture')
        elif n.type().name() == 'comp':
            run_mplay(n,'copoutput')
        elif n.type().name() == 'ris::22':
            run_mplay(n,'ri_display_0')

    elif switch == True:
        if n.type().name() == 'ifd':
            run_rv(n,'vm_picture')        
        elif n.type().name() == 'opengl':
            run_rv(n,'picture')
        elif n.type().name() == 'arnold':
            run_rv(n,'ar_picture')
        elif n.type().name() == 'comp':
            run_rv(n,'copoutput')
        elif n.type().name() == 'ris::22':
            run_rv(n,'ri_display_0')

    # else:
    #     hou.ui.displayMessage('Plz select Mantra ROP')

def run_mplay(n,nparm):
    mplay = hou.expandString("$HFS") + "/bin/mplay"
    path = n.parm(nparm).evalAsString()
    fps = '-r {}'.format(hou.fps())
    #options = None
    if n.parm('trange').eval()!=0:
        pathSplit = path.split(".")
        pathSplit[-2] = "$F"
        path = ".".join(pathSplit)
        #options = ' -f {} {} {}'.format(n.parm('f1').eval(),n.parm('f2').eval(),n.parm('f3').eval())    
    args = [mplay, fps, path]
    #print(args)
    subprocess.Popen(args)


def run_rv(n,nparm):

    rv = "/opt/rv-Linux-x86-64-7.1.0/bin/rv"
    fps = '-fps {}'.format(hou.fps())
    options = ''
    path = n.parm(nparm).evalAsString()
    if n.parm('trange').eval()!=0:
        pathSplit = path.split(".")
        pathSplit[-2] = "#"
        path = ".".join(pathSplit)
        #options = '%d-%d' % (n.evalParm('f1'),n.evalParm('f2'))
    
    cmd = "%s %s %s %s" % (rv, fps, options, path)    
    #args = [rv, path]
    #print(args)
    #subprocess.call(args)
    #subprocess.call( cmd.strip().split(" ")  )
    subprocess.Popen( cmd.strip().split(" ")  )
    #uvl.wait()
#launch_mplay()