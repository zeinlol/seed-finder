from core.config.minecraft_config import game


def generate_random_seed():
    return game.mojangapi.world.WorldSeed.random()
