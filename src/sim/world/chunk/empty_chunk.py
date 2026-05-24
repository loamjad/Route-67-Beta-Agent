from src.sim.world.chunk.chunk import Chunk

class EmptyChunk(Chunk):
    def __init__(self, world_in, x, z):
        super().__init__(world_in, x, z)