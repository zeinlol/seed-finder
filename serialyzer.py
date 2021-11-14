mesa = [37, 39, 167, 38, 166, 165]


def filter_mesa(biome_array):
    return all(mesa_id not in biome_array for mesa_id in mesa)
