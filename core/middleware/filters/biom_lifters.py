from core.config.typing import T_BIOMES_LIST


def filter_biome(biomes_array, target_biome=T_BIOMES_LIST):
    return all(biome.biome_id not in biomes_array for biome in target_biome)

