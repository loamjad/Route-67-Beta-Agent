from src.sim.init.blocks import Blocks
from src.sim.world.chunk.storage.extended_block_storage import ExtendedBlockStorage

class Chunk:
    def __init__(self, world_in=None, x=0, z=0):
        # TODO: Implement
        self.storage_arrays = []
        self.height_map = []
        self.is_chunk_loaded = True
        self.world_obj = world_in
        self.x_position = x
        self.z_position = z

    def get_block_state(self, pos):
        try:
            if pos.get_y() >= 0 and pos.get_y() >> 4 < len(self.storage_arrays):
                extendedblockstorage = self.storage_arrays[pos.get_y() >> 4]

                if extendedblockstorage != None:
                    j = pos.get_x() & 15
                    k = pos.get_y() & 15
                    i = pos.get_z() & 15
                    return extendedblockstorage.get(j, k, i)
                
            return Blocks.air.get_default_state()
        except:
            pass

    def set_block_state(self, pos, state):
        i = pos.get_x() & 15
        j = pos.get_y()
        k = pos.get_z() & 15
        l = k << 4 | i
        i1 = self.height_map[l]

        iblockstate = self.get_block_state(pos)
        if iblockstate == state:
            return None
        else:
            block = state.get_block()
            block1 = iblockstate.get_block()
            extendedblockstorage = self.storage_arrays[j >> 4]
            # flag = False

            if extendedblockstorage is None:
                if block == Blocks.air:
                    return None
                
                self.storage_arrays[j >> 4] = ExtendedBlockStorage(j >> 4 << 4)
                extendedblockstorage = self.storage_arrays[j >> 4]
                
                flag = j >= i1

            extendedblockstorage.set(i, j & 15, k, state)

            # if self.world_obj is not None and not self.world_obj.is_remote:
            #     if block1 != block:
            #         block1.break_block(self.world_obj, pos, iblockstate)

            # if extendedblockstorage.get_block_by_ext_id(i, j & 15, k) != block:
            #     return None

            # if self.world_obj is not None and not self.world_obj.is_remote and block1 != block:
            #     block.on_block_added(self.world_obj, pos, state)

            self.is_modified = True
            return iblockstate

    def set_chunk_loaded(self, loaded):
        self.is_chunk_loaded = loaded