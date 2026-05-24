import numpy as np

from src.sim.init.blocks import Blocks
from src.sim.util.math_helper import MathHelper
from src.sim.util.block_pos import BlockPos

class World:
    def __init__(self):
        self.chunk_provider = None
        self.is_remote = None

    def is_valid(self, pos):
        pass

    def get_block_state(self, pos):
        if not self.is_valid(pos):
            return Blocks.air.get_default_state()
        else:
            chunk = Blocks.get_chunk_from_block_coords(pos)
            return chunk.get_block_state(pos)
        
    def get_chunk_from_block_coords(self, pos):
        return Blocks.get_chunk_from_chunk_coords(pos.get_x() >> 4, pos.get_z() >> 4)
    
    def get_chunk_from_chunk_coords(self, chunk_x, chunk_z):
        return Blocks.chunk_provider.provideChunk(chunk_x, chunk_z)
    
    def get_colliding_bounding_boxes(self, entity_in, bb):
        list = []
        i = MathHelper.floor_double(bb.min_x)
        j = MathHelper.floor_double(bb.max_x + np.float64(1.0))
        k = MathHelper.floor_double(bb.min_y)
        l = MathHelper.floor_double(bb.max_y + np.float64(1.0))
        i1 = MathHelper.floor_double(bb.min_z)
        j1 = MathHelper.floor_double(bb.max_z + np.float64(1.0))
        iblockstate = Blocks.stone.get_default_state()
        blockpos_mutableblockpos = BlockPos.MutableBlockPos()

        for k1 in range(i, j):
            for l1 in range(i1, j1):
                # if self.is_block_loaded(blockpos_mutableblockpos.set(k1, 64, l1)):
                for i2 in range(k - 1, l):
                    blockpos_mutableblockpos.set(k1, i2, l1)

                    iblockstate1 = iblockstate

                    iblockstate1 = self.get_block_state(blockpos_mutableblockpos)

                    iblockstate1.get_block().add_collision_boxes_to_list(self, blockpos_mutableblockpos, iblockstate1, bb, list, entity_in)

        return list

