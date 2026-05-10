from src.sim.init.blocks import Blocks

class World:
    def __init__(self):
        self.chunk_provider = None
        self.is_remote = None

    def is_valid(self, pos):
        pass

    def get_block_state(self, pos):
        if not World.is_valid(pos):
            return Blocks.air
        else:
            chunk = Blocks.get_chunk_from_block_coords(pos)
            return chunk.get_block_state(pos)
        
    def get_chunk_from_block_coords(self, pos):
        return Blocks.get_chunk_from_chunk_coords(pos.get_x() >> 4, pos.get_z() >> 4)
    
    def get_chunk_from_chunk_coords(self, chunk_x, chunk_z):
        return Blocks.chunk_provider.provideChunk(chunk_x, chunk_z)
    

        
