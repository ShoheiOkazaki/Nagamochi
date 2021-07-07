import re
import os
import hou

def RightReplace( fullString, oldString, newString, occurences ):
    return newString.join( fullString.rsplit( oldString, occurences ) )


def convertPathWithPad(outputFile,regularexp=False):
    paddedNumberRegex = re.compile( "([0-9]+)", re.IGNORECASE )
    #outputFile = cnode.parm(parm).eval()
    matches = paddedNumberRegex.findall( os.path.basename( outputFile ) )

    if matches != None and len( matches ) > 0:
        paddingString = matches[ len( matches ) - 1 ]
        paddingSize = len( paddingString )
        if regularexp:
            padding = '%{:02d}d'.format(paddingSize)
        else:
            padding = "#"
            while len(padding) < paddingSize:
                padding = padding + "#"
        paddedOutputFile = RightReplace( outputFile, paddingString, padding, 1 )
        
    return paddedOutputFile


