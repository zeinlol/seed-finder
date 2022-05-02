from abc import ABC, abstractmethod

from core.config.typing import T_BIOME_IDS


class AbstractAssetClass(ABC):
    @abstractmethod
    def get_biomes_ids(self) -> T_BIOME_IDS:
        """ return biome signatures."""
        ...

