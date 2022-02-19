import os
import datetime
import sys

import hou
import nodesearch

def MSG(text_name,text_body,date_enable=True,print_enbale=True,StatusMessage_enbale=False,StatusMessage_type=hou.severityType.Message):
    
    dt_now = datetime.datetime.now()
    startDate= dt_now.strftime('%Y-%m-%d %H:%M:%S')

    msg = '[Nagamochi][{}] {}'.format(text_name,text_body)

    if date_enable:
        msg = '{}  {}'.format(startDate,msg)

    if print_enbale:
        print(msg)

    if StatusMessage_enbale:
        hou.ui.setStatusMessage(msg,severity=StatusMessage_type)

    return msg

def reload_func(func_name):
    if sys.version_info[0]>2:
        import importlib
        importlib.reload(func_name)
    else:
        reload(func_name)
