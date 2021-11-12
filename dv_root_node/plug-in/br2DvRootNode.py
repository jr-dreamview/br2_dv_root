"""This module provides a plugin that defines a custom maya transform node for use in
identifying and managing assets from ShotGrid via file_collection and tasks.
In order for the node to be available in maya, the plug-ins directory where this file is
located must be found in the MAYA_PLUG_IN_PATH for the environment under which maya is launched.
"""


import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


pluginName = "br2DvRootNode"
nodeName = "BR2DvRootNode"
nodeId = OpenMaya.MTypeId(0x00138942)
matrixId = OpenMaya.MTypeId(0x00138943)
NODE_VERSION = "1.0"

# keep track of instances of DvRootMatrix to get
# around script limitation with proxy classes of
# base pointers that point to derived classes.
kTrackingDictionary = {}


class DvRootMatrix(OpenMayaMPx.MPxTransformationMatrix):
    """Custom Transform matrix class associated with the DvRootNode transform plugin.
    This class is  required by the Transform plugin system. The current implementation
    is a wrapper around the transform matrix class used by maya's native Transform node,
    and provides no additional functionality.
    """

    def __init__(self):
        """Initializer."""
        OpenMayaMPx.MPxTransformationMatrix.__init__(self)
        kTrackingDictionary[OpenMayaMPx.asHashable(self)] = self

    def __del__(self):
        """Deletes the instance"""
        del kTrackingDictionary[OpenMayaMPx.asHashable(self)]


class DvRootNode(OpenMayaMPx.MPxTransform):
    """Custom maya transform node for identifying and managing assets from ShotGrid imported into maya scenes.
    The node is used to identify transforms that represent imported assets from ShotGrid,
    and to provide information needed to export changes made to that content to the correct locations.
    """

    # Define variables used to define the node's custom attributes.
    asset_name = OpenMaya.MObject()
    asset_type = OpenMaya.MObject()
    date_created = OpenMaya.MObject()
    deliverable_id = OpenMaya.MObject()
    dpack_id = OpenMaya.MObject()
    fc_id = OpenMaya.MObject()
    file_name = OpenMaya.MObject()
    file_type = OpenMaya.MObject()
    node_version = OpenMaya.MObject()
    project = OpenMaya.MObject()
    project_id = OpenMaya.MObject()
    status = OpenMaya.MObject()
    task = OpenMaya.MObject()
    task_id = OpenMaya.MObject()
    user = OpenMaya.MObject()
    user_id = OpenMaya.MObject()
    version = OpenMaya.MObject()

    def __init__(self, transform=None):
        """Initializer.
        Args:
            transform (OpenMayaMPx.MPxTransform): If given the new instance is initialized
                as a copy of the given instance. Defaults to None.
        """
        if transform is None:
            OpenMayaMPx.MPxTransform.__init__(self)
        else:
            OpenMayaMPx.MPxTransform.__init__(self, transform)

    def className(self):
        """The name of the custom node type.
        Returns:
            str: Node name.
        """
        return nodeName

    def createTransformationMatrix(self):
        """Creates a new transform node.
        Returns:
            MPxPtr: Pointer to the newly minted transform node.
        """
        return OpenMayaMPx.asMPxPtr(DvRootMatrix())


def initializePlugin(mobject):
    """Registers the DvRootNode plugin.
    Args:
        mobject (OpenMaya.MObject): Maya object instance representing the DvRootNode plug in.
    """
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    mplugin.registerTransform(
        pluginName, nodeId,
        nodeCreator, nodeInitializer, matrixCreator,
        matrixId)


def uninitializePlugin(mobject):
    """Unregisters the DvRootNode plugin.
    Args:
        mobject (OpenMaya.MObject): Maya object instance representing the DvRootNode plug in.
    """
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    mplugin.deregisterNode(nodeId)


# create/initialize node and matrix
def matrixCreator():
    """Creates a transform matrix node for a newly minted DvRooNode.
    Returns:
        MPxPtr: Pointer to new transform matrix node.
    """
    return OpenMayaMPx.asMPxPtr(DvRootMatrix())


def nodeCreator():
    """Creates a new DvRootNode.
    Returns:
        MPxPtr: Pointer to the newly minted transform node.
    """
    return OpenMayaMPx.asMPxPtr(DvRootNode())


def nodeInitializer():
    """Initializes a newly minted DvRootNode.
    All custom attributes are defined and associated with the new node by this function.
    """
    asset_name_attr = OpenMaya.MFnTypedAttribute()
    DvRootNode.asset_name = asset_name_attr.create(
        "Asset_Name", "asset_name",
        OpenMaya.MFnData.kString,
        OpenMaya.MFnStringData().create(""))
    DvRootNode.addAttribute(DvRootNode.asset_name)

    dpack_id_attr = OpenMaya.MFnNumericAttribute()
    DvRootNode.dpack_id = dpack_id_attr.create(
        "Deliverable_Package_ID", "dpack_id",
        OpenMaya.MFnNumericData.kInt)
    DvRootNode.addAttribute(DvRootNode.dpack_id)

    project_attr = OpenMaya.MFnTypedAttribute()
    DvRootNode.project = project_attr.create(
        "Project", "project",
        OpenMaya.MFnData.kString,
        OpenMaya.MFnStringData().create(""))
    DvRootNode.addAttribute(DvRootNode.project)

    project_id_attr = OpenMaya.MFnNumericAttribute()
    DvRootNode.project_id = project_id_attr.create(
        "Project_ID", "project_id",
        OpenMaya.MFnNumericData.kInt)
    DvRootNode.addAttribute(DvRootNode.project_id)

    task_attr = OpenMaya.MFnTypedAttribute()
    DvRootNode.task = task_attr.create(
        "Task", "task",
        OpenMaya.MFnData.kString,
        OpenMaya.MFnStringData().create(""))
    DvRootNode.addAttribute(DvRootNode.task)

    task_id_attr = OpenMaya.MFnNumericAttribute()
    DvRootNode.task_id = task_id_attr.create(
        "Task_ID", "task_id",
        OpenMaya.MFnNumericData.kInt)
    DvRootNode.addAttribute(DvRootNode.task_id)

    type_attr = OpenMaya.MFnTypedAttribute()
    DvRootNode.asset_type = type_attr.create(
        "Asset_Type", "asset_type",
        OpenMaya.MFnData.kString,
        OpenMaya.MFnStringData().create(""))
    DvRootNode.addAttribute(DvRootNode.asset_type)

    version_attr = OpenMaya.MFnTypedAttribute()
    DvRootNode.version = version_attr.create(
        "Version", "version",
        OpenMaya.MFnData.kString,
        OpenMaya.MFnStringData().create(""))
    DvRootNode.addAttribute(DvRootNode.version)

    file_collection_id_attr = OpenMaya.MFnNumericAttribute()
    DvRootNode.file_collection_id = file_collection_id_attr.create(
        "File_Collection_ID", "fc_id",
        OpenMaya.MFnNumericData.kInt)
    DvRootNode.addAttribute(DvRootNode.file_collection_id)

    status_attr = OpenMaya.MFnTypedAttribute()
    DvRootNode.status = status_attr.create(
        "Status", "status",
        OpenMaya.MFnData.kString,
        OpenMaya.MFnStringData().create(""))
    DvRootNode.addAttribute(DvRootNode.status)

    file_name_attr = OpenMaya.MFnTypedAttribute()
    DvRootNode.file_name = file_name_attr.create(
        "File_Name", "file_name",
        OpenMaya.MFnData.kString,
        OpenMaya.MFnStringData().create(""))
    DvRootNode.addAttribute(DvRootNode.file_name)

    file_type_attr = OpenMaya.MFnTypedAttribute()
    DvRootNode.file_type = file_type_attr.create(
        "File_Type", "file_type",
        OpenMaya.MFnData.kString,
        OpenMaya.MFnStringData().create(""))
    DvRootNode.addAttribute(DvRootNode.file_type)

    user_attr = OpenMaya.MFnTypedAttribute()
    DvRootNode.user = user_attr.create(
        "User", "user",
        OpenMaya.MFnData.kString,
        OpenMaya.MFnStringData().create(""))
    DvRootNode.addAttribute(DvRootNode.user)

    user_id_attr = OpenMaya.MFnNumericAttribute()
    DvRootNode.user_id = user_id_attr.create(
        "User_ID", "user_id",
        OpenMaya.MFnNumericData.kInt)
    DvRootNode.addAttribute(DvRootNode.user_id)

    date_created_attr = OpenMaya.MFnTypedAttribute()
    DvRootNode.date_created = date_created_attr.create(
        "Date_Created", "date_created",
        OpenMaya.MFnData.kString,
        OpenMaya.MFnStringData().create(""))
    DvRootNode.addAttribute(DvRootNode.date_created)

    node_version_attr = OpenMaya.MFnTypedAttribute()
    DvRootNode.node_version = node_version_attr.create(
        "Node_Version", "node_version",
        OpenMaya.MFnData.kString,
        OpenMaya.MFnStringData().create(NODE_VERSION))
    DvRootNode.addAttribute(DvRootNode.node_version)
