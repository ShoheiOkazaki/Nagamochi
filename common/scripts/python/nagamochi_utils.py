import os
import datetime
import sys
import re

import hou
import nodesearch

def MSG(text_name,text_body,date_enable=True,print_enbale=True,StatusMessage_enbale=False,StatusMessage_type=hou.severityType.Message):
    """
    Logs a message with various options for displaying and logging the message.

    Parameters:
    - text_name: A brief name or category for the message.
    - text_body: The main content of the message.
    - date_enable: If True, prefix the message with the current date and time.
    - print_enable: If True, print the message to the console.
    - status_message_enable: If True, display the message as a status message in Houdini.
    - severity_type: The severity type for the status message in Houdini.
    """

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
    

def reload_func(module):
    """
    Reloads the specified module. Compatible with both Python 2 and 3.

    Parameters:
    - module: The module to reload.
    """
    if sys.version_info[0] > 2:
        import importlib
        importlib.reload(module)
    else:
        reload(module)


def remove_prefixes(name, prefixes):
    """
    Removes specified prefixes from a given name.

    Parameters:
    - name: The original name string.
    - prefixes: A list of prefix strings to be removed.

    Returns:
    - The name with specified prefixes removed.
    """
    pattern = r"^(?:" + "|".join(prefixes) + ")_+"
    return re.sub(pattern, "", name)



def get_shelf_tool_script(shelf_name, tool_name):
    """
    Retrieves the script of a Tool from the specified Shelf and Tool names.

    Parameters:
    - shelf_name: The name of the Shelf where the Tool resides.
    - tool_name: The name of the Tool whose script is to be retrieved.

    Return:
    - The script of the specified Shelf Tool. Returns None if the Tool is not found.
    """
    # Retrieve all shelves
    shelves = hou.shelves.shelves()

    # Search for the specified Shelf
    shelf = shelves.get(shelf_name)
    if not shelf:
        print(f"Shelf '{shelf_name}' not found.")
        return None

    # Retrieve tools from the specified Shelf
    tools = shelf.tools()

    # Search for the specified Tool within the Shelf
    tool = next((t for t in tools if t.name() == tool_name), None)
    if not tool:
        print(f"Tool '{tool_name}' not found in shelf '{shelf_name}'.")
        return None

    # Retrieve the Tool's script
    script = tool.script()
    return script

# # Usage example
# shelf_name = "nm_customnodes"  # Insert the name of your Shelf here
# tool_name = "nm_nul_addparm"   # Insert the name of your Tool here
# script = get_shelf_tool_script(shelf_name, tool_name)
# if script:
#     print("Tool Script:\n", script)
