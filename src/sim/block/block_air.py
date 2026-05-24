from src.sim.block.material import Material
from src.sim.block.block import Block

class BlockAir(Block):
    def __init__(self):
        super().__init__(Material.air)

    def get_collision_bounding_box(self, world_in, pos, state):
        return None
    
    def can_collide_check(self, state, hit_if_liquid):
        return False