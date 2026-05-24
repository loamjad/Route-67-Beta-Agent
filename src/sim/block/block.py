import numpy as np

from src.sim.util.axis_aligned_bb import AxisAlignedBB
from src.sim.block.material import Material
from src.sim.block.state.block_state import BlockState

class Block:
    def __init__(self, material: Material):
        self.block_material = material
        self.slipperiness = np.float32(0.6)
        self.default_block_state = None
        self.min_x = np.float64(0.0)
        self.min_y = np.float64(0.0)
        self.min_z = np.float64(0.0)
        self.max_x = np.float64(1.0)
        self.max_y = np.float64(1.0)
        self.max_z = np.float64(1.0)

        self.block_state = BlockState(self)
        self.set_default_state(self.block_state.get_base_state())

    def get_default_state(self):
        return self.default_block_state
    
    def set_default_state(self, state):
        self.default_block_state = state

    def add_collision_boxes_to_list(self, world_in, pos, state, mask, list, colliding_entity):
        axisalignedbb = self.get_collision_bounding_box(world_in, pos, state)
        if axisalignedbb is not None and mask.intersects_with(axisalignedbb):
            list.append(axisalignedbb)

    def on_landed(self, world_in, entity_in) -> None:
        entity_in.motion_y = np.float64(0.0)

    def on_fallen_upon(self, world_in, pos, entity_in, fall_distance: np.float32) -> None:
        entity_in.fall(fall_distance, np.float32(1.0))

    def get_material(self) -> Material:
        return self.block_material

    def on_entity_collided_with_block(self, world_in, pos, entity_in) -> None:
        pass

    def get_collision_bounding_box(self, world_in, pos, state):
        return AxisAlignedBB(
            pos.get_x() + self.min_x, pos.get_y() + self.min_y, pos.get_z() + self.min_z,
            pos.get_x() + self.max_x, pos.get_y() + self.max_y, pos.get_z() + self.max_z
        )