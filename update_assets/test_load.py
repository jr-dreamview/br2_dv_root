import os
import sys

maya_path = r"C:\Users\john.russell\Code\git_stuff\dreamview-studios-inc\DreamViewStudios\application\maya"
if maya_path not in sys.path:
    sys.path.append(maya_path)
from br2.dv_root_node.node_handler import MayaRootHandler
from br2.update_assets.test_version_swap import reference_and_reparent


files = [
    {
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
    },
    {
        "name_dpack": r"ERAS_0101_CRT1_0320_Shot_Anim",
        "path_file": r"V:/Shot/ERAS_0101_CRT1_0320/Shot Anim/maya/other/ERAS_0101_CRT1_0320_Shot_Anim_V020.abc",
        "version_fc": "12",
        "task": "Shot Anim",
        "project": "Bleacher Report",
        "id_dpack": 21963,
        "id_fc": 92720,
        "id_project": 1039,
        "id_task": 69374,
        "id_user": 1083,
        "status": "wip",
        "type_asset": "Character",
        "user": "Aerik Bertulfo",
        "date_created": "2021-05-11 22:01:28+00:00"
    },
    {
        "name_dpack": r"ERAS_0101_CRT1_0320_Shot_Camera",
        "path_file": r"V:/Shot/ERAS_0101_CRT1_0320/Shot_Camera/maya/scenes/CRT1_0320_Camera_V001.ma",
        "version_fc": "1",
        "task": "Shot_Camera",
        "project": "Bleacher Report",
        "id_dpack": 21966,
        "id_fc": 86261,
        "id_project": 1039,
        "id_task": 69377,
        "id_user": 1190,
        "status": "wip",
        "type_asset": "Camera",
        "user": "An Nguyen",
        "date_created": "2021-04-16 01:57:58+00:00"
    }]

for f in files:
    node = MayaRootHandler.create(
        f.get("name_dpack"),
        asset_type=f.get("type_asset"),
        date_created=f.get("date_created"),
        dpack_id=f.get("id_dpack"),
        fc_id=f.get("id_fc"),
        status=f.get("status"),
        file_name=os.path.basename(f.get("path_file")),
        file_type=os.path.splitext(f.get("path_file"))[-1],
        project=f.get("project"),
        project_id=f.get("id_project"),
        version=f.get("version_fc"),
        task=f.get("task"),
        task_id=f.get("id_task"),
        user=f.get("user"),
        user_id=f.get("id_user")).dag_name,
    new_reference_nodes = reference_and_reparent(f.get("path_file"), node)
