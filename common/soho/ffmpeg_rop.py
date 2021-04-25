import soho
import subprocess

from nagamochi_utils import MSG
script_name = 'FFmpeg_ROP'

get_ffmpeg     = soho.getDefaultedString("ffmpeg_path",[""])[0]
get_inputfile  = soho.getDefaultedString("ff_inputfile_with_pad",[""])[0]
get_inputArgs  = soho.getDefaultedString("ff_inputArgs",[""])[0]
get_outArgs    = soho.getDefaultedString("ff_outputArgs",[""])[0]
get_outputfile = soho.getDefaultedString("ff_outputFile",[""])[0]


cmd1 = '{} {} -i "{}" {} -y "{}"'.format(get_ffmpeg, get_inputArgs, get_inputfile, get_outArgs, get_outputfile)

MSG( script_name,'[FFmpeg_ROP] {}'.format(cmd1) )

subprocess.call(cmd1, shell=True)