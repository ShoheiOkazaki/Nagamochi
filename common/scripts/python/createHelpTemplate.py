#----------------------------------------------------------------------------------------------------
#     Name: createTemplateHelp
#  Version: 1.0
# Released: 2015.02.09
#    Autor: Shohei
#  Enabled: 14.0.227
#----------------------------------------------------------------------------------------------------
# Create help txt on $HIP. It is usefull to create otl's help.
#----------------------------------------------------------------------------------------------------
# v1.0 - main release
#----------------------------------------------------------------------------------------------------

import hou
from datetime import datetime, date, time

from nagamochi_utils import MSG
script_name = 'createHelpTemplate'

def doit():

    # selected node
    nodes = hou.selectedNodes()
    
    if len(nodes) > 0:
        
        # just first one
        node = nodes[0]
        # Parameter types to ignore.
        to_ignore = (hou.parmTemplateType.Separator,
                     hou.parmTemplateType.Label,
                     hou.parmTemplateType.FolderSet,
                    )
                    
        # Folder name to ignore
        ignore_folder = ('Deadline',
                         '(Invisible Param)',
                         'invisible'
                         )


        nodetype = node.type()
        description = nodetype.description()
        #type_name = nodetype.name()
        type_name = nodetype.nameComponents()[-2]
        version = nodetype.nameComponents()[-1]

        # Start the list.
        result = ["#type: node"]

        context = nodetype.category().name().lower()

        # Create the header information
        result.append("#context: %s" % context)
        icon = nodetype.icon().replace("_", "/", 1)
        result.append("#icon: %s" % icon)
        result.append("#internal: %s" % type_name)
        result.append("#version: %s" % version)

        # Create the title block.
        result.append("")
        result.append("= %s =" % description)
        result.append("")

        result.append('"""Enter Description Here"""')
        result.append("")

        # Parameters block.
        result.append("@parameters")


        count = 0

        previous_folders = ()
        for parm_tuple in node.parmTuples():
            template = parm_tuple.parmTemplate()
            
            
            # If this parm is a type to ignore, skip to the next one.
            if template.type() in to_ignore:
                continue
            #print template
            folders = parm_tuple[0].containingFolders()


            
            folder_len = len(folders)
            prev_len = len(previous_folders)
            ignore = False 
            # If there are containing folders we need to generate folder entries.
            if folder_len > 0:
                # The folder is different than the folder of the previous parm.
                if folders != previous_folders:
                    # If the number of folders is equal we need to find where the changes
                    # are occuring.
                    if folder_len == prev_len:
                        # Change index.
                        idx = 0
                        # Iterate through all the
                        for i in range(folder_len):
                            # If the current folder differs at this index, set the index
                            # and break.
                            if folders[i] != previous_folders[i]:
                                idx = i
                                break

                        # Start from where they began to differ and iterate forward to add
                        # in missing entries.
                        for i in range(idx, folder_len - 1):
                            result.append("%s== %s == " % ("    " * i, folders[i]))
                            result.append("%sEnter a Folder Description" % ("    " * (i+1)))
                            result.append("")

                    # If the current folder is less deep than the previous one we need to check
                    # to see if they still share hierarchy so as to not add extra folder entries.
                    elif folder_len < prev_len:
                        diff = prev_len - folder_len
                        # If the current folder is equal to the folder in the previous list minus
                        # the difference in length, then we need to ignore adding the new entry.
                        if folders[-1] == previous_folders[-(diff + 1)]:
                            ignore = True

                    if not ignore:
                        # Add an entry.
                        result.append("%s== %s ==" % ("    " * (folder_len - 1), folders[-1]))
                        result.append("%sEnter a folder Description" % ("    " * (folder_len)))
                        result.append("")
                        previous_folders = folders


            parm_template = parm_tuple.parmTemplate()
            if parm_template.isHidden():
                continue
            # Print the parm tuple name as a title for the parameter name.
            result.append("%s%s:"
                   % ('    ' * folder_len, parm_tuple.description().replace("_", " ").title()))
            # Try and get the help text.
            help_txt = parm_tuple.parmTemplate().help()
            # If there is help text, use it as the description.
            if len(help_txt) > 0:
                result.append("%s%s" % ('    ' * (folder_len + 1), help_txt))
            # If not, insert the place holder.
            else:
                result.append("%sEnter a parameter description" % ('    ' * (folder_len + 1)))
                result.append("")

            # If this parm is a menu parm we need to add entries for each label.
            if template.type() == hou.parmTemplateType.Menu:
                labels = template.menuLabels()
                for label in labels:
                    result.append("%s%s:" % ('    ' * (folder_len + 1), label))
                    result.append("%sEnter a parameter description" % ('    ' * (folder_len + 2)))    

        # ReleaseNote block.
        result.append("@release Release Note")
        username = hou.expandString('$USERNAME')
        if username == '':
            username = hou.expandString('$USER')

        noteHeader = '{} - {} - {} - {} :'.format(version, datetime.now().strftime("%Y/%m/%d"), hou.applicationVersionString(), username)
        result.append(noteHeader)
        result.append("	:new: Initial Release")


        # Export txt file to $HIP
        txtPath = hou.expandString('$HIP') + "/" + type_name + ".txt"
        meg_txt = 'Save to ' + txtPath
        MSG(script_name,meg_txt,StatusMessage_enbale=True)
        texts = '\n'.join(result)
        f = open(txtPath,'w')
        f.writelines(texts)
        f.close()

        hou.ui.copyTextToClipboard(texts)

    # if nothing to select
    else:
        hou.ui.displayMessage("Please select any node.", buttons=('Yes', 'No'))

    
#createTemplateHelp()
