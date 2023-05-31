import subprocess
import hou

target_list = {
        'ifd' : 'vm_picture',
        'opengl': 'picture',
        'arnold' : 'ar_picture',
        'comp' : 'copoutput',
        'ris' : 'ri_display_0',
        'ffmpeg': 'ff_outputFile',
        'nmFlipbook' : 'soho_diskfile'
        }


def launch(switch):   

    ns = hou.selectedNodes()

    for n in ns:
        node_type_name = n.type().nameComponents()[2]

        if switch == False:
            run_mplay(n, target_list[node_type_name])       

        elif switch == True:
            run_rv(n, target_list[node_type_name])  

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

    rv = hou.getenv("NM_RV_PATH")
    fps = '-fps {}'.format(hou.fps())
    options = ''
    path = n.parm(nparm).evalAsString()
    if n.parm('trange').eval()!=0:
        pathSplit = path.split(".")
        pathSplit[-2] = "#"
        path = ".".join(pathSplit)
        #options = '%d-%d' % (n.evalParm('f1'),n.evalParm('f2'))
    
    cmd = "%s %s %s" % (rv, fps, path)    
    #args = [rv, path]
    #print(args)
    #subprocess.call(args)
    #subprocess.call( cmd.strip().split(" ")  )
    subprocess.Popen( cmd.strip().split(" ")  )
    #uvl.wait()
