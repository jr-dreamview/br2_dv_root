

FILE_COLLECTIONS = [
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


class AssetData(object):
    def __init__(self, asset_dict):
        self.dict = asset_dict

        self.date_created1 = asset_dict.get("date_created")
        self.dpack_id1 = asset_dict.get("id_dpack")
        self.fc_id1 = asset_dict.get("id_fc")
        self.path_file1 = asset_dict.get("path_file")
        self.status1 = asset_dict.get("status")
        self.user1 = asset_dict.get("user")
        self.version_fc1 = asset_dict.get("version_fc")

    @property
    def date_created(self):
        return self.date_created1

    @date_created.setter
    def date_created(self, val):
        self.date_created1 = val

    @property
    def dpack_id(self):
        return self.dpack_id1

    @dpack_id.setter
    def dpack_id(self, val):
        self.dpack_id1 = val

    @property
    def fc_id(self):
        return self.fc_id1

    @fc_id.setter
    def fc_id(self, val):
        self.fc_id1 = val

    @property
    def path_file(self):
        return self.path_file1

    @path_file.setter
    def path_file(self, val):
        self.path_file1 = val

    @property
    def status(self):
        return self.status1

    @status.setter
    def status(self, val):
        self.status1 = val

    @property
    def user(self):
        return self.user1

    @user.setter
    def user(self, val):
        self.user1 = val

    @property
    def version_fc(self):
        return self.version_fc1

    @version_fc.setter
    def version_fc(self, val):
        self.version_fc1 = val


def get_file_collection_data(fc_id):
    for f in FILE_COLLECTIONS:
        if fc_id == f.get("id_fc"):
            return AssetData(f)
    return None


def get_versions_data(dpack_id):
    return [AssetData(f) for f in FILE_COLLECTIONS if f.get("dpack_id") == dpack_id]
