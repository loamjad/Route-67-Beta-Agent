from src.sim.init.blocks import Blocks
from src.sim.block.block import Block

class ExtendedBlockStorage:
    def __init__(self, y):
        self.y_base = y
        self.data = []

    def get(self, x, y, z):
        iblockstate = self.data[y << 8 | z << 4 | x]
        return iblockstate if iblockstate != None else Blocks.air.get_default_state()