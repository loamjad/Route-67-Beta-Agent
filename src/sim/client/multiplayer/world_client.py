from src.sim.world.world import World
from src.sim.client.multiplayer.chunk_provider_client import ChunkProviderClient

class WorldClient(World):
    def __init__(self):
        self.client_chunk_provider = None
        self.mc = None

        self.chunk_provider = self.create_chunk_provider()

    def create_chunk_provider(self):
        self.client_chunk_provider = ChunkProviderClient(self)
        return self.client_chunk_provider
    
