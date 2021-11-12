import sys

maya_path = r"C:\Users\john.russell\Code\git_stuff\dreamview-studios-inc\DreamViewStudios\application\maya"
if maya_path not in sys.path:
    sys.path.append(maya_path)

from br2.dv_root_node.node_handler import MayaRootHandler

import maya.cmds as cmds


class Asset(object):
    def __init__(self):
        pass


def reference_and_reparent(filepath, parent_node=None):
    """Imports the maya scene residing at filepath, and re-parents the contents to parent_node.

    Args:
        filepath (str): Filepath.
        parent_node (None|str): Name of parent node to which contents are to re-parent.

    Returns:
        None|str: New reference node.
    """
    existing_ref_nodes = cmds.ls(type="reference")
    top_level_nodes_before = cmds.ls(assemblies=True)
    file_type = cmds.file(filepath, query=True, type=True)[0]
    try:
        imported_nodes = cmds.file(
            filepath,
            reference=True,
            type=file_type,
            ignoreVersion=True,
            mergeNamespacesOnClash=True,
            namespace=":",
            groupLocator=False,
            returnNewNodes=True,
            options="v=1")
    except RuntimeError:
        print("Possible problem with referenced file: {}".format(filepath))
        return

    top_level_nodes_after = cmds.ls(assemblies=True)

    imported_top_level_nodes = list(set(top_level_nodes_after) - set(top_level_nodes_before))

    if parent_node is not None:
        for node in imported_top_level_nodes:
            if cmds.nodeType(node) == "transform":
                # TODO: Is there a way to lock just the transform attrs of nodes
                #   from the reference file.  Normal locking of individual
                #   attributes apparently isn't allowed.  And using 'file'
                #   command's -lockReferences flag prevent reparenting
                #   the contents.

                node_parent = cmds.listRelatives(node, parent=True, fullPath=True)
                if node_parent is None:
                    cmds.parent(node, parent_node, relative=True)

    ref_nodes = cmds.ls(type="reference")
    new_ref_nodes = list(set(ref_nodes) - set(existing_ref_nodes))

    return new_ref_nodes[0]


def swap_version(node, new_version):
    unload_ref(node)
    reference_and_reparent(new_version.path_file, node)
    update_root_node(node, new_version)


def unload_ref(node):
    reference_nodes = []
    children = cmds.listRelatives(node, fullPath=True)
    for c in children:
        try:
            rn = cmds.referenceQuery(c, referenceNode=True)
        except:
            print("Not good: {}".format(c))
            continue
        if rn and rn not in reference_nodes:
            reference_nodes.append(rn)

    if not reference_nodes:
        return

    reference_node = reference_nodes[0]

    for c in children:
        cmds.parent(c, removeObject=True)
    cmds.file(unloadReference=reference_node)
    cmds.file(removeReference=True, referenceNode=reference_node)


def update_root_node(node, new_version):
    node_handler = MayaRootHandler(node)
    node_handler.version = new_version.version_fc
    node_handler.fc_id = new_version.fc_id
    node_handler.status = new_version.status
    node_handler.date_created = new_version.date_created
    node_handler.user = new_version.user
    

if __name__ == "__main__":
    ver_26 = {
        "name_dpack": r"KDurant_Base_LookDev",
        "path_file": r"V:/Asset/KDurant/LookDev/maya/scenes/KDurant_Base_lookDev_V026.ma",
        "version_fc": "26",
        "task": "LookDev",
        "project": "Bleacher Report",
        "id_dpack": 16938,
        "id_fc": 91754,
        "id_project": 1039,
        "id_task": 63126,
        "id_user": 263,
        "status": "wip",
        "type_asset": "Character",
        "user": "Brian Freisinger",
        "date_created": "2021-05-07 23:06:04+00:00"
    }

    ver_27 = {
        "name_dpack": r"KDurant_Base_LookDev",
        "path_file": r"V:/Asset/KDurant/LookDev/maya/scenes/KDurant_Base_lookDev_V027.ma",
        "version_fc": "27",
        "task": "LookDev",
        "project": "Bleacher Report",
        "id_dpack": 16938,
        "id_fc": 101963,
        "id_project": 1039,
        "id_task": 63126,
        "id_user": 263,
        "status": "wip",
        "type_asset": "Character",
        "user": "Brian Freisinger",
        "date_created": "2021-07-06 22:27:40+00:00"
    }

    node = "KDurant_Base_lookDev"

    node_ver = ver_27

    swap_version(node, node_ver)
