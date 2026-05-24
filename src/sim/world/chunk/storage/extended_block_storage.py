from src.sim.init.blocks import Blocks
from src.sim.block.block import Block

class ExtendedBlockStorage:
    def __init__(self, y):
        self.y_base = y
        self.data = [None] * 4096
        self.block_ref_count = 0
        self.tick_ref_count = 0

    def get(self, x, y, z):
        iblockstate = self.data[y << 8 | z << 4 | x]
        return iblockstate if iblockstate is not None else Blocks.air.get_default_state()

    def set(self, x, y, z, state) -> None:
        iblockstate = self.get(x, y, z)
        block = iblockstate.get_block()
        block1 = state.get_block()

        # if block != Blocks.air:
        #     self.block_ref_count -= 1
        #       if block.get_tick_randomly():
        #           self.tick_ref_count -= 1

        # if block1 != Blocks.air:
        #     self.block_ref_count += 1
        #       if block1.get_tick_randomly():
        #           self.tick_ref_count += 1

        self.data[y << 8 | z << 4 | x] = state