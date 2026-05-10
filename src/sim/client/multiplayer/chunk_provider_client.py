from src.sim.world.chunk.empty_chunk import EmptyChunk
from src.sim.world.chunk.chunk import Chunk
from src.sim.world.chunk_coord_int_pair import ChunkCoordIntPair
from src.sim.util.long_hash_map import LongHashMap

class ChunkProviderClient:
    def __init__(self, world_in):
        self.blank_chunk = EmptyChunk(world_in, 0, 0)
        self.chunk_mapping = LongHashMap()
        self.chunk_listing = []

        self.blank_chunk = EmptyChunk(world_in, 0, 0)
        self.world_obj = world_in

    def load_chunk(self, x, z):
        chunk = Chunk(self.world_obj, x, z)
        self.chunk_mapping.add(ChunkCoordIntPair.chunk_XZ2_int(x, z), chunk)
        self.chunk_listing.add(chunk)
        chunk.set_chunk_loaded(True)
        return chunk