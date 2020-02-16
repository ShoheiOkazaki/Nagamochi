
import hou
import os

def setDefalut(selRops):
    #selRops = hou.selectedNodes()
    

    if len(selRops)>0:
        

        selRop = selRops[0]
        parmnum = [0]   
        jobName = 'Render++++__`$OS` (`chs("version")`)'

        folder_img_render = "$HIP/../render"
        folder_img_flipbook = "$HIP/../render"
        folder_texture = "$HIP/../texture"
        folder_cache = "$HIP/../cache"

        

        renderpath = "{}/`$OS`/`chs('version')`/beauty/${{OS}}.`chs('version')`.$F4.exr".format(folder_img_render)
        flippath = "{}/flipbook/`$OS`/`chs('version')`/`$OS`.`chs('version')`.$F4.jpg".format(folder_img_flipbook)

        if selRop.type().name()=='ifd':
            selRop.setParms({
                # Images
                "vm_picture": renderpath,#Output Picture
                "vm_dcmfilename": renderpath.replace('${OS}.','${OS}_deep.'),
                "vm_writecheckpoint":0,
                #Rendering
                "vm_renderengine": "pbrraytrace", # Rendering Engine
                "vm_samplesx" : 2,                  # Pixel Samples
                "vm_samplesy" : 2,                  # Pixel Samples
                #"vm_variance" : 0.07,               # Noise Level
                "vm_transparentsamples" : 16,
                #"vm_reflectlimit" : 2,
                #"vm_refractlimit" : 2,
                "vm_colorlimit" : 5,
                "vm_alfprogress" : 1,
                # Objects
                "soho_autoheadlight" : 0,
                #Driver
                #"soho_diskfile" : '$HIP/ifds/`$OS`/`chs("versionMajor")`_`chs("versionMinor")`/`$OS`.`chs("versionMajor")`_`chs("versionMinor")`.$F4.ifd',
                #"vm_tmpsharedstorage": "$HIP/ifds/$OS/`chs('versionMajor')`_`chs('versionMinor')`/storage",
                "vm_tmplocalstorage" : "$HOUDINI_TEMP_DIR/ifds/storage/$OS",
                # Harvester
                #"job_title" : "Hou Mantra [ $OS - `chs('ver')` ]",
                })
            if hou.getenv('CAM_WORK'):
                selRop.parm('camera').set('$CAM_WORK')

            exp_df = "import os\nn=hou.pwd()\nfile=hou.getenv('HIP')\nfolder=os.path.dirname(file)\nuser=hou.getenv('USER')\nreturn ( '{0}/../cache/{4}/ifd/{1}/{2}/{1}.{2}.{3:04d}.ifd'.format(folder,n.name(),n.evalParm('version'),int(hou.frame()),user) )"
            exp_sts = "import os\nn=hou.pwd()\nfile=hou.getenv('HIP')\nfolder=os.path.dirname(file)\nuser=hou.getenv('USER')\nreturn ('{0}/../cache/{1}/ifd/{2}/{3}/storage'.format(folder,user,n.name(),n.evalParm('version')))"
            selRop.parm('soho_diskfile').setExpression(exp_df,hou.exprLanguage.Python)
            selRop.parm('vm_tmpsharedstorage').setExpression(exp_sts,hou.exprLanguage.Python)

            try:
                selRop.parm('dl_jobName').set(jobName.replace('++++',selRop.type().description()))
            except:
                pass
            parmnum[0] += 8

        elif selRop.type().name()=='arnold':
            #jobName = '`$OS`(`chs("versionMajor")`)'

            selRop.setParms({
                # Main              
                # Properties
                #  - Output
                "ar_picture": renderpath, #Output Picture
                "ar_exr_half_precision" : 1,
                # "ar_exr_color_family" : 'Input/ARRI', #20181225
                # "ar_exr_color_space":'Input - ARRI - Linear - ALEXA Wide Gamut',  #20181225                                   # Half Precision
                #  - Sampling
                # "ar_AA_samples" : 2,                                               # Camera (AA)
                # "ar_GI_diffuse_samples" : 0,                                     # Diffuse
                # "ar_GI_specular_samples" : 0,                                      # Glossy
                # "ar_GI_transmission_samples" : 1,                                 # Glossy
                # "ar_GI_sss_samples" : 0,                                     # SSS
                # "ar_GI_volume_samples" : 2,                               # Volume Indirect
                #  - Ray Depth
                #"ar_auto_transparency_threshold" : 0.650,                      # Transp. Threshold     
                #  - Motion Blur
                "ar_mb_shutter" : "center",                                        # Shutter Position 'start',''
                #  - Textures
                "ar_texture_max_memory_MB" : 2048.0,                             # Cache Size (MB)
                "ar_texture_use_existing_tx" : 1,                                # Use Existing .tx Textures
                "ar_texture_accept_untiled" : 1,
                #  - System
                "ar_abort_on_license_fail":1,
                #  - Diagnostics
                "ar_log_verbosity" : "detailed",                                 #  Log Verbosity
                "ar_ignore_operators":1, # For Igonre Input
                # Archive
                "ar_binary_ass" : 0,
                "ar_export_asstoc" : 0,
                "ar_prepend_htoa_paths" : 0,
                
                })

            if hou.getenv('CAM_WORK'):
                selRop.parm('camera').set('$CAM_WORK')

            exp_ass = "import os\nn=hou.pwd()\nfile=hou.getenv('HIP')\nfolder=os.path.dirname(file)\nuser=hou.getenv('USER')\nreturn ( '{0}/../cache/ass/{1}/{2}/{1}.{2}.{3:04d}.ass'.format(folder,n.name(),n.evalParm('version'),int(hou.frame())) )"
            selRop.parm('ar_ass_file').setExpression(exp_ass,hou.exprLanguage.Python)

            try:
                selRop.parm('dl_jobName').set(jobName.replace('++++',selRop.type().description()))
            except:
                pass

            # * Arnold Set Defalut AOVs
            ar_aovs = {
                                'A':['deepexr','FLOAT','beauty'],
                                'P':['beauty','RGB','closest_filter'],
                                'Z':['beauty','FLOAT','closest_filter'],
                   'diffuse_direct':['beauty','RGB','beauty'],
                 'diffuse_indirect':['beauty','RGB','beauty'],
                  'specular_direct':['beauty','RGB','beauty'],
                'specular_indirect':['beauty','RGB','beauty'],
                       'sss_direct':['beauty','RGB','beauty'],
                     'sss_indirect':['beauty','RGB','beauty'],
                     'transmission':['beauty','RGB','beauty'],
                    'volume_direct':['beauty','RGB','beauty'],
                  'volume_indirect':['beauty','RGB','beauty'],
                   'volume_opacity':['beauty','RGB','beauty'],
                }

            selRop.parm('ar_aovs').set(len(ar_aovs))
            ar_aov_num = 1
            for arAovName,arAovAttr in ar_aovs.items():
                selRop.setParms({
                    'ar_aov_label{}'.format(ar_aov_num):arAovName,
                    'ar_aov_picture_format{}'.format(ar_aov_num):arAovAttr[0],
                    'ar_aov_type{}'.format(ar_aov_num):arAovAttr[1],
                    'ar_aov_pixel_filter{}'.format(ar_aov_num):arAovAttr[2],
                    'ar_aov_separate{}'.format(ar_aov_num):0,
                    #'ar_aov_separate_file{}'.format(ar_aov_num):"$HIP/../render/`$OS`/`chs('version')`/`chs('ar_aov_label{0}')`/`$OS`_`chs('ar_aov_label{0}')`.`chs('version')`.$F4.exr".format(ar_aov_num),
                    'ar_enable_aov{}'.format(ar_aov_num):0,
                    })
                ar_aov_num += 1

            parmnum[0] += 6

        elif selRop.type().name()=='vray' or selRop.type().name()=='vray_renderer':
            selRop.setParms({
                "render_camera" : "$CAM_WORK",
                "SettingsOutput_img_dir" : renderpath.rsplit('/',1)[0],
                "SettingsOutput_img_file" : renderpath.rsplit('/',1)[1],
                "SettingsImageSampler_dmc_maxSubdivs" : 8,
                "SettingsDMCSampler_use_local_subdivs": True,
                "SettingsGI_on" : False,
                "SettingsRTEngine_max_render_time":1,
                })
            parmnum[0] += 8

        elif selRop.type().name()=='opengl':
            selRop.setParms({
                "picture" : flippath,
                "gamma" : 2.2,
                #"sopsource" : 0,
                #"aamode" : 0,
                #"usehdr" : 0,
                #"shadows" : 0,
                #"shadowquality" : 0,
                #"transquality" : 1,
                })
            if hou.getenv('CAM_WORK'):
                selRop.parm('camera').set('$CAM_WORK')
            try:
                selRop.parm('dl_jobName').set(jobName.replace('++++',selRop.type().description()))
                selRop.parm('dl_jobGroup').set('box')
            except:
                pass
            parmnum[0] += 6

        elif selRop.type().name()=='baketexture::3.0':
            selRop.setParms({
                "vm_uvoutputpicture1" : "{}/`$OS`/`chs('version')`/`$OS`.`chs('version')`_%(CHANNEL)s.%(UDIM)d.$F4.tga".format(folder_texture),
                })
            parmnum[0] += 8

        elif selRop.type().name()=='PRT_ROPDriver':
            selRop.setParms({
                "file" : "{}/prt/`$OS`/`chs('version')`/`$OS`.`chs('version')`.$F.prt".format(folder_cache)
                })
            try:
                jobName = 'BakeKrakatoaPRT__`$OS` (`chs("version")`)'
                selRop.parm('dl_jobName').set(jobName)              
            except:
                pass
            parmnum[0] += 6

        firstTime = 0       

        for pn in selRop.parms():
            if pn.name() == "versionMajor":
                firstTime += 1
                break

        if firstTime == 0:
            # add [ver] parm if doent exit
            defaMajVer = "v001"
            defaMinVer = "01"

            if hou.getenv('MAJVER')!= None and hou.ui.displayMessage("Choose Versioning Method", buttons=("Use Variable", "Custom"), severity=hou.severityType.Message, title="[Nagamochi] Render Default")==0:
                defaMajVer = "v$MAJVER"
                defaMinVer = "$MINVER"  
            #addMajParm = eval('hou.%sParmTemplate("%s", "%s", 1,default_value=(["%s"]))' % ('String', 'versionMajor', 'Version Major', defaMajVer))
            #addMinParm = eval('hou.%sParmTemplate("%s", "%s", 1,default_value=(["%s"]))' % ('String', 'versionMinor', 'Version Minor', defaMinVer))
            addVerParm = eval('hou.%sParmTemplate("%s", "%s", 1,default_value=(["%s"]))' % ('String', 'version', 'Version ', defaMajVer))

            parm = selRop.parms()[parmnum[0]]
            parmTmp = parm.parmTemplate()
            parmGroup = selRop.parmTemplateGroup()
            parmIndex = parmGroup.findIndices(parmTmp.name())[0]
            parmGroup.insertAfter(parmGroup.parmTemplates()[parmIndex],addVerParm)
            #parmGroup.insertAfter(parmGroup.parmTemplates()[parmIndex+1],addMinParm)
            selRop.setParmTemplateGroup(parmGroup)

