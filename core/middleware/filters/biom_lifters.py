from core.config.constants.bioms_id import MESA_IDS
from core.config.typing import T_BIOME_IDS


def filter_biome(biomes_array, target_biome=T_BIOME_IDS):
    return all(biome_id not in biomes_array for biome_id in target_biome)


def filter_mesa(biomes_array):
    return filter_biome(biomes_array=biomes_array, target_biome=MESA_IDS)
