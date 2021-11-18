from os import path

from config.variables import amidst_file


def get_newest_asset() -> list[path]:
    # TODO analyze assets folder and choose best match (by amid version or by amid & minecraft versions)
    return [path.join("assets", amidst_file)]
