from config.minecraft_config import game


def get_minecraft_versions() -> list:
    new_minecraft_instance = game.mojangapi.file.MinecraftInstallation.newLocalMinecraftInstallation()
    return list(new_minecraft_instance.readInstalledVersionsAsLauncherProfiles())
