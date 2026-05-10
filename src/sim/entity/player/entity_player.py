import numpy as np

from src.sim.entity.entity_living_base import EntityLivingBase
from src.sim.entity.shared_monster_attributes import SharedMonsterAttributes
from src.sim.util.block_pos import BlockPos


class EntityPlayer(EntityLivingBase):
    def __init__(self):
        # The current location of the player
        self.player_location: BlockPos = None
        self.speed_on_ground = np.float32(0.1)
        self.speed_in_air = np.float32(0.02)

        super().__init__()
        

    def on_update(self):
        super().on_update()

    def on_living_update(self):
        super().on_living_update()
        iattributeinstance = self.get_entity_attribute(SharedMonsterAttributes.movement_speed)

        self.jump_movement_factor = self.speed_in_air

        if self.is_sprinting():
            self.jump_movement_factor = np.float32(np.float64(self.jump_movement_factor) + np.float64(self.speed_in_air) * np.float64(0.3))

        self.set_AI_move_speed(iattributeinstance.get_attribute_value())

    def update_entity_action_state(self):
        super().update_entity_action_state()

    def apply_entity_attributes(self):
        super().apply_entity_attributes()
        self.get_entity_attribute(SharedMonsterAttributes.movement_speed).set_base_value(np.float64(0.10000000149011612))

    

