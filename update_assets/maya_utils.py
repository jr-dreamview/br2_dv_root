import sys

maya_path = r"C:\Users\john.russell\Code\git_stuff\dreamview-studios-inc\DreamViewStudios\application\maya"
if maya_path not in sys.path:
    sys.path.append(maya_path)

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI


def get_all_dv_root_nodes():
    """Returns a list of names of all DvRootNodes in the scene.

    Returns:
        list[str]: List of names of all DvRootNodes in the scene.
    """
    return cmds.ls(type="br2DvRootNode")


def get_main_window_ptr():
    """Get the pointer to Maya main window.

    Returns:
        SwigPyObject: Pointer to main window.
    """
    return apiUI.MQtUtil.mainWindow()
