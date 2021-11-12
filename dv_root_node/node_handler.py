import logging
import os

import maya.cmds as cmds


LOGGER = logging.getLogger(__name__)
ROOT_NODE_TYPE = "br2DvRootNode"


class MayaRootHandler:
    """Handler class for interacting with DvRootNodes.
    DvRootNodes are custom maya transform nodes used to represent Usd Entity
    Resources imported into maya. This node handler class provides convenient
    access to the DvRootNode's custom attributes which provide information used
    to identify an imported Resource, and determine it's repository locations.
    """
    def __init__(self, node):
        """Initializer.

        Args:
            node (str): The name of an existing DvRootNode in the calling maya session.
        Raises:
            WorkspaceError: If given a node that can not be found in the calling maya
                session.
            WorkspaceError: If given a node that is not a DvRootNode.
        """
        # Load root node plugin.
        load_root_plugin()

        # Confirm node exists.
        if not cmds.objExists(node):
            raise RuntimeError(f'"{node}" not found.')

        # Confirm node is of expected type.
        if not cmds.nodeType(node) == ROOT_NODE_TYPE:
            raise RuntimeError(f'"{node}" is not a dvRootNode.')

        # Initialize state.
        self._uuid = cmds.ls(node, uuid=True)[0]

    @property
    def asset_name(self):
        """The name of the Resource represented by the instance.

        Returns:
            str: Resource name.
        """
        return cmds.getAttr(f"{self.dag_path}.asset_name")

    @asset_name.setter
    def asset_name(self, value):
        """Sets the name attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Resource name.
        """
        attr = f"{self.dag_path}.asset_name"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value, type="string")
        cmds.setAttr(attr, lock=True)

    @property
    def asset_type(self):
        """The asset_type of the Resource represented by the instance.

        Returns:
            str: Resource asset_type.
        """
        return cmds.getAttr(f"{self.dag_path}.asset_type")

    @asset_type.setter
    def asset_type(self, value):
        """Sets the asset_type attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Resource name.
        """
        attr = f"{self.dag_path}.asset_type"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value, type="string")
        cmds.setAttr(attr, lock=True)

    @property
    def dag_name(self):
        """The short node name of the DvRootNode managed by the instance.

        Returns:
            str: Node name.
        """
        return self.dag_path.split("|")[-1]

    @dag_name.setter
    def dag_name(self, name):
        """Sets the short name of the DvRootNode managed by the instance.

        Args:
            name (str): Node name.
        """
        cmds.rename(self.dag_path, name)

    @property
    def dag_path(self):
        """The full DAG path to the DvRootNode managed by the instance.

        Returns:
            str: DAG path.
        """
        path = cmds.ls(self._uuid, uuid=True, long=True)
        if path:
            return path[0]

        # No root node found. It may have been deleted from
        # the calling maya session while the MayaRootHandler instance
        # if still in use.
        scene = cmds.file(query=True, sceneName=True)
        raise RuntimeError(f'Unable to locate root node: {self._uuid} in "{scene}"')

    @property
    def date_created(self):
        """The asset_type of the Resource represented by the instance.

        Returns:
            str: Resource asset_type.
        """
        return cmds.getAttr(f"{self.dag_path}.date_created")

    @date_created.setter
    def date_created(self, value):
        """Sets the asset_type attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Resource name.
        """
        attr = f"{self.dag_path}.date_created"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value, type="string")
        cmds.setAttr(attr, lock=True)

    @property
    def dpack_id(self):
        """The Repository Project associated with the Entity represented by the instance.

        Returns:
            str: Project name.
        """
        return cmds.getAttr(f"{self.dag_path}.dpack_id")

    @dpack_id.setter
    def dpack_id(self, value):
        """Sets the Project attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Project name.
        """
        attr = f"{self.dag_path}.dpack_id"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value)
        cmds.setAttr(attr, lock=True)

    @property
    def fc_id(self):
        """The Repository Project associated with the Entity represented by the instance.

        Returns:
            str: Project name.
        """
        return cmds.getAttr(f"{self.dag_path}.fc_id")

    @fc_id.setter
    def fc_id(self, value):
        """Sets the Project attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Project name.
        """
        attr = f"{self.dag_path}.fc_id"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value)
        cmds.setAttr(attr, lock=True)

    @property
    def file_name(self):
        """The asset_type of the Resource represented by the instance.

        Returns:
            str: Resource asset_type.
        """
        return cmds.getAttr(f"{self.dag_path}.file_name")

    @file_name.setter
    def file_name(self, value):
        """Sets the asset_type attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Resource name.
        """
        attr = f"{self.dag_path}.file_name"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value, type="string")
        cmds.setAttr(attr, lock=True)

    @property
    def file_type(self):
        """The asset_type of the Resource represented by the instance.

        Returns:
            str: Resource asset_type.
        """
        return cmds.getAttr(f"{self.dag_path}.file_type")

    @file_type.setter
    def file_type(self, value):
        """Sets the asset_type attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Resource name.
        """
        attr = f"{self.dag_path}.file_type"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value, type="string")
        cmds.setAttr(attr, lock=True)

    @property
    def node_version(self):
        """The Version of the Resource represented by the instance.

        Returns:
            str: Version specifier.
        """
        return cmds.getAttr(f"{self.dag_path}.node_version")

    @node_version.setter
    def node_version(self, value):
        """Sets the Version attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Version Specifier.
        """
        attr = f"{self.dag_path}.node_version"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value, type="string")
        cmds.setAttr(attr, lock=True)

    @property
    def project(self):
        """The Repository Project associated with the Entity represented by the instance.

        Returns:
            str: Project name.
        """
        return cmds.getAttr(f"{self.dag_path}.project")

    @project.setter
    def project(self, value):
        """Sets the Project attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Project name.
        """
        attr = f"{self.dag_path}.project"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value, type="string")
        cmds.setAttr(attr, lock=True)

    @property
    def project_id(self):
        """The Repository Project associated with the Entity represented by the instance.

        Returns:
            str: Project name.
        """
        return cmds.getAttr(f"{self.dag_path}.project_id")

    @project_id.setter
    def project_id(self, value):
        """Sets the Project attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Project name.
        """
        attr = f"{self.dag_path}.project_id"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value)
        cmds.setAttr(attr, lock=True)

    @property
    def status(self):
        """The Repository Project associated with the Entity represented by the instance.

        Returns:
            str: Project name.
        """
        return cmds.getAttr(f"{self.dag_path}.status")

    @status.setter
    def status(self, value):
        """Sets the Project attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Project name.
        """
        attr = f"{self.dag_path}.status"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value, type="string")
        cmds.setAttr(attr, lock=True)

    @property
    def task(self):
        """The Repository Project associated with the Entity represented by the instance.

        Returns:
            str: Project name.
        """
        return cmds.getAttr(f"{self.dag_path}.task")

    @task.setter
    def task(self, value):
        """Sets the Project attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Project name.
        """
        attr = f"{self.dag_path}.task"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value, type="string")
        cmds.setAttr(attr, lock=True)

    @property
    def task_id(self):
        """The Repository Project associated with the Entity represented by the instance.

        Returns:
            str: Project name.
        """
        return cmds.getAttr(f"{self.dag_path}.task_id")

    @task_id.setter
    def task_id(self, value):
        """Sets the Project attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Project name.
        """
        attr = f"{self.dag_path}.task_id"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value)
        cmds.setAttr(attr, lock=True)

    @property
    def user(self):
        """The asset_type of the Resource represented by the instance.

        Returns:
            str: Resource asset_type.
        """
        return cmds.getAttr(f"{self.dag_path}.user")

    @user.setter
    def user(self, value):
        """Sets the asset_type attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Resource name.
        """
        attr = f"{self.dag_path}.user"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value, type="string")
        cmds.setAttr(attr, lock=True)

    @property
    def user_id(self):
        """The asset_type of the Resource represented by the instance.

        Returns:
            str: Resource asset_type.
        """
        return cmds.getAttr(f"{self.dag_path}.user_id")

    @user_id.setter
    def user_id(self, value):
        """Sets the asset_type attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Resource name.
        """
        attr = f"{self.dag_path}.user_id"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value)
        cmds.setAttr(attr, lock=True)

    @property
    def uuid(self):
        """The maya UUID of the DvRootNode managed by the instance.

        Returns:
            str: UUID.
        """
        return self._uuid

    @property
    def version(self):
        """The Version of the Resource represented by the instance.

        Returns:
            str: Version specifier.
        """
        return cmds.getAttr(f"{self.dag_path}.version")

    @version.setter
    def version(self, value):
        """Sets the Version attribute on the DVRootNode managed by the instance.

        Args:
            value (str): Version Specifier.
        """
        attr = f"{self.dag_path}.version"
        cmds.setAttr(attr, lock=False)
        cmds.setAttr(attr, value, type="string")
        cmds.setAttr(attr, lock=True)

    @classmethod
    def create(cls, name, dpack_id=0, project="", project_id=0, task="", task_id=0, asset_type="", version="",
               fc_id=0, status="", file_name="", file_type="", user="", user_id=0, date_created=""):
        """Creates a new DvRootNode.

        Args:
            name (str): Node name.
            dpack_id (int): Deliverable package.  Defaults to "".
            project (str): Project name. Defaults to "".
            project_id (int):  Project ID.  Defaults to 0.
            task (str): Task.  Defaults to "".
            task_id (int):  Task_id.  Default to 0.
            asset_type (str): Asset Type.  Default to ""
            version (str): Version string. Defaults to "".
            fc_id (int): FileCollection ID.  Defaults to 0.
            status (str): Status.  Defaults to "".
            file_name (str): File name.  Defaults to "".
            file_type (str): File type.  Defaults to "".
            user (str): User name.  Defaults to "".
            user_id (int): User ID.  Defaults to 0.
            date_created (str): Date created.  Defaults to "".
        Returns:
            MayaRootHandler: Handler.
        """
        # Load root node plugin.
        load_root_plugin()

        # Create root node and initialize handler.
        node = cls(cmds.createNode(ROOT_NODE_TYPE, name=name))

        # Set handler attrs.
        node.asset_name = name
        node.asset_type = asset_type
        node.date_created = date_created
        node.dpack_id = dpack_id
        node.fc_id = fc_id
        node.file_name = file_name
        node.file_type = file_type
        node.project = project
        node.project_id = project_id
        node.status = status
        node.task = task
        node.task_id = task_id
        node.user = user
        node.user_id = user_id
        node.version = version

        cmds.setAttr(f"{node.dag_path}.node_version", lock=True)

        return node

    def iter_child_roots(self, recursive=False):
        """An iterator over all the Root's child Root Nodes.

        Args:
            recursive (bool, optional): If True yield children of children, otherwise
                yield only direct children. Defaults to False.
        Yields:
            MayaRootHandler: Child Root.
        """
        if recursive:
            children = cmds.listRelatives(self.dag_path, allDescendents=True, type=ROOT_NODE_TYPE)
        else:
            children = cmds.listRelatives(self.dag_path, children=True, type=ROOT_NODE_TYPE)
        for child in children or []:
            yield self.__class__(child)

    def iter_parent_roots(self, recursive=False):
        """An iterator over the Root's parent Root nodes.

        Args:
            recursive (bool, optional): If True yield parents of parents, otherwise
                yield only the direct parent. Defaults to False.
        Yields:
            MayaRootHandler: Parent Root.
        """
        node = self.dag_path
        while node:
            node = cmds.listRelatives(node, parent=True, fullPath=True)
            if node:
                node = node[0]
                if cmds.nodeType(node) == ROOT_NODE_TYPE:
                    yield self.__class__(node)
                    if not recursive:
                        break

    @classmethod
    def iter_world_roots(cls):
        """An iterator over all roots in the calling maya scene parented under world.

        Yields:
            MayaRootHandler: Root.
        """
        for node in cmds.ls(type=ROOT_NODE_TYPE, long=True) or []:
            if not cmds.listRelatives(node, parent=True):
                yield cls(node)

    def __eq__(self, other):
        """Defines the equality comparison operator for the instance.

        Args:
            other (object): Object to compare.
        Returns:
            [bool]: True if other is a MayaRootHandler instance initialized with the same DAG path.
        """
        return self.__class__ == other.__class__ and self.dag_path == other.dag_path

    def __str__(self):
        """Provides the string representation of the instance.

        Returns:
            str: String representation.
        """
        return f'{self.__class__.__name__}("{self.dag_path}")'


def add_plugin_path():
    """"""
    node_plugin_path = os.path.join(os.path.dirname(__file__), "plug-in")
    mpp = os.environ.get("MAYA_PLUG_IN_PATH")
    if mpp is None:
        os.environ["MAYA_PLUG_IN_PATH"] = node_plugin_path
    elif node_plugin_path not in mpp:
        os.environ["MAYA_PLUG_IN_PATH"] = ";".join([node_plugin_path, mpp])


def load_root_plugin():
    """Loads the dvRootNode plugin if it has not already been loaded."""
    add_plugin_path()
    if not cmds.pluginInfo(ROOT_NODE_TYPE, query=True, loaded=True):
        cmds.loadPlugin(ROOT_NODE_TYPE)
