from src.sim.block.material import Material
from src.sim.block.block import Block

class BlockStone(Block):
    def __init__(self):
        super().__init__(Material.rock)
        self.set_default_state(self.block_state.get_base_state())