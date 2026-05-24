import numpy as np
import math

from src.sim.util.axis_aligned_bb import AxisAlignedBB
from src.sim.entity.data_watcher import DataWatcher
from src.sim.util.math_helper import MathHelper
from src.sim.util.block_pos import BlockPos
from src.sim.block.material import Material


class Entity:
    def __init__(self, world_in):
        ZERO_AABB = AxisAlignedBB(np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0))
        self.world_obj = None
        self.prev_pos_x = np.float64(0.0)
        self.prev_pos_y = np.float64(0.0)
        self.prev_pos_z = np.float64(0.0)
        self.pos_x = np.float64(0.0)
        self.pos_y = np.float64(0.0)
        self.pos_z = np.float64(0.0)
        self.motion_x = np.float64(0.0)
        self.motion_y = np.float64(0.0)
        self.motion_z = np.float64(0.0)
        self.rotation_yaw = np.float32(0.0)
        self.rotation_pitch = np.float32(0.0)
        self.prev_rotation_yaw = np.float32(0.0)
        self.prev_rotation_pitch = np.float32(0.0)
        self.bounding_box = ZERO_AABB
        self.on_ground = True
        self.is_collided_horizontally = False
        self.is_collided_vertically = False
        self.is_collided = False
        self.is_in_web = False
        self.width = np.float32(0.6)
        self.height = np.float32(1.8)
        self.nextStepDistance = 1
        self.step_height = np.float32(0.0)
        self.ticks_existed = 0
        self.in_water = False
        self.data_watcher = DataWatcher(self)
        self.is_air_borne = False
        
        self.world_obj = world_in
        self.set_position(np.float64(0.0), np.float64(0.0), np.float64(0.0))
        self.data_watcher.add_object(0, np.int8(0))
        self.data_watcher.add_object(1, np.int16(300))
        self.data_watcher.add_object(3, np.int8(0))
        self.data_watcher.add_object(2, "")
        self.data_watcher.add_object(4, np.int8(0))






        self.last_tick_pos_x = np.float64(0.0)
        self.last_tick_pos_y = np.float64(0.0)
        self.last_tick_pos_z = np.float64(0.0)
        


        self.prev_rotation_yaw = np.float32(0.0)
        self.prev_rotation_pitch = np.float32(0.0)
        self.distance_walked_modified = np.float32(0.0)
        self.prev_distance_walked_modified = np.float32(0.0)
        self.distance_walked_on_step_modified = np.float32(0.0)
        self.next_step_distance = 1
        self.fall_distance = np.float32(0.0)
        self.first_update = True

    def set_position(self, x, y, z):
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z
        f = self.width/np.float32(2.0)
        f1 = self.height
        self.set_entity_bounding_box(
            AxisAlignedBB(
                x - np.float64(f),
                y,
                z - np.float64(f),
                x + np.float64(f),
                y + np.float64(f1),
                z + np.float64(f)
            )
        )

    def set_entity_bounding_box(self, bb: AxisAlignedBB):
        self.bounding_box = bb

    def get_jump_upwards_motion(self):
        return np.float32(0.42)

    def jump(self):
        self.motion_y = self.get_jump_upwards_motion()
        self.is_air_borne = True

    def move_entity(self, x, y, z):
        d0 = self.pos_x
        d1 = self.pos_y
        d2 = self.pos_z

        d3 = x
        d4 = y
        d5 = z
        flag = self.on_ground and self.is_sneaking()

        if flag:
            d6 = np.float64(0.0)

        list1 = self.world_obj.get_colliding_bounding_boxes(self, self.get_entity_bounding_box().add_coord(x, y, z))
        axisalignedbb = self.get_entity_bounding_box()

        for axisalignedbb1 in list1:
            y = axisalignedbb1.calculate_y_offset(self.get_entity_bounding_box(), y)

        self.set_entity_bounding_box(self.get_entity_bounding_box().offset(np.float64(0.0), y, np.float64(0.0)))
        flag1 = self.on_ground or (d4 != y and d4 < np.float64(0.0))

        for axisalignedbb2 in list1:
            x = axisalignedbb2.calculate_x_offset(self.get_entity_bounding_box(), x)

        self.set_entity_bounding_box(self.get_entity_bounding_box().offset(x, np.float64(0.0), np.float64(0.0)))

        for axisalignedbb3 in list1:
            z = axisalignedbb3.calculate_z_offset(self.get_entity_bounding_box(), z)

        self.set_entity_bounding_box(self.get_entity_bounding_box().offset(np.float64(0.0), np.float64(0.0), z))

        if self.step_height > np.float32(0.0) and flag1 and (d3 != x or d5 != z):
            d11 = x
            d7 = y
            d8 = z
            axisalignedbb_step = self.get_entity_bounding_box()
            self.set_entity_bounding_box(axisalignedbb)
            y = np.float64(self.step_height)
            list2 = self.world_obj.get_colliding_bounding_boxes(self, self.get_entity_bounding_box().add_coord(d3, y, d5))
            axisalignedbb4 = self.get_entity_bounding_box()
            axisalignedbb5 = axisalignedbb4.add_coord(d3, np.float64(0.0), d5)
            d9 = y

            for axisalignedbb6 in list2:
                d9 = axisalignedbb6.calculate_y_offset(axisalignedbb5, d9)

            axisalignedbb4 = axisalignedbb4.offset(np.float64(0.0), d9, np.float64(0.0))
            d15 = d3

            for axisalignedbb7 in list2:
                d15 = axisalignedbb7.calculate_x_offset(axisalignedbb4, d15)

            axisalignedbb4 = axisalignedbb4.offset(d15, np.float64(0.0), np.float64(0.0))
            d16 = d5

            for axisalignedbb8 in list2:
                d16 = axisalignedbb8.calculate_z_offset(axisalignedbb4, d16)

            axisalignedbb4 = axisalignedbb4.offset(np.float64(0.0), np.float64(0.0), d16)
            axisalignedbb14 = self.get_entity_bounding_box()
            d17 = y

            for axisalignedbb9 in list2:
                d17 = axisalignedbb9.calculate_y_offset(axisalignedbb14, d17)

            axisalignedbb14 = axisalignedbb14.offset(np.float64(0.0), d17, np.float64(0.0))
            d18 = d3

            for axisalignedbb10 in list2:
                d18 = axisalignedbb10.calculate_x_offset(axisalignedbb14, d18)

            axisalignedbb14 = axisalignedbb14.offset(d18, np.float64(0.0), np.float64(0.0))
            d19 = d5

            for axisalignedbb11 in list2:
                d19 = axisalignedbb11.calculate_z_offset(axisalignedbb14, d19)

            axisalignedbb14 = axisalignedbb14.offset(np.float64(0.0), np.float64(0.0), d19)
            d20 = d15 * d15 + d16 * d16
            d10 = d18 * d18 + d19 * d19

            if d20 > d10:
                x = d15
                z = d16
                y = -d9
                self.set_entity_bounding_box(axisalignedbb4)
            else:
                x = d18
                z = d19
                y = -d17
                self.set_entity_bounding_box(axisalignedbb14)

            for axisalignedbb12 in list2:
                y = axisalignedbb12.calculate_y_offset(self.get_entity_bounding_box(), y)

            self.set_entity_bounding_box(self.get_entity_bounding_box().offset(np.float64(0.0), y, np.float64(0.0)))

            if d11 * d11 + d8 * d8 >= x * x + z * z:
                x = d11
                y = d7
                z = d8
                self.set_entity_bounding_box(axisalignedbb_step)

        self.reset_position_to_BB()
        self.is_collided_horizontally = d3 != x or d5 != z
        self.is_collided_vertically = d4 != y
        self.on_ground = self.is_collided_vertically and d4 < np.float64(0.0)
        self.is_collided = self.is_collided_horizontally or self.is_collided_vertically
        i = MathHelper.floor_double(self.pos_x)
        j = MathHelper.floor_double(self.pos_y - np.float64(0.20000000298023224))
        k = MathHelper.floor_double(self.pos_z)
        blockpos = BlockPos(i, j, k)
        block1 = self.world_obj.get_block_state(blockpos).get_block()

        if block1.get_material() == Material.air:
            block = self.world_obj.get_block_state(blockpos.down()).get_block()
            # if isinstance(block, (BlockFence, BlockWall, BlockFenceGate)):
            #     block1 = block
            #     blockpos = blockpos.down()

        self.update_fall_state(y, self.on_ground, block1, blockpos)

        if d3 != x:
            self.motion_x = np.float64(0.0)

        if d5 != z:
            self.motion_z = np.float64(0.0)

        if d4 != y:
            block1.on_landed(self.world_obj, self)

        if self.can_trigger_walking() and not flag:
            d12 = self.pos_x - d0
            d13 = self.pos_y - d1
            d14 = self.pos_z - d2
            if True: #block1 != Blocks.ladder
                d13 = np.float64(0.0)
            if block1 is not None and self.on_ground:
                block1.on_entity_collided_with_block(self.world_obj, blockpos, self)
            self.distance_walked_modified = np.float32(np.float64(self.distance_walked_modified) + np.float64(MathHelper.sqrt_double(d12 * d12 + d14 * d14)) * np.float64(0.6))
            self.distance_walked_on_step_modified = np.float32(np.float64(self.distance_walked_on_step_modified) + np.float64(MathHelper.sqrt_double(d12 * d12 + d13 * d13 + d14 * d14)) * np.float64(0.6))
            if self.distance_walked_on_step_modified > np.float32(self.next_step_distance) and block1.get_material() != Material.air:
                self.next_step_distance = int(self.distance_walked_on_step_modified) + 1

        # try:
        #     self.do_block_collisions()
        # except Exception as throwable:
        #     crashreport = CrashReport.make_crash_report(throwable, "Checking entity block collision")
        #     crashreportcategory = crashreport.make_category("Entity being checked for collision")
        #     self.add_entity_crash_info(crashreportcategory)
        #     raise ReportedException(crashreport)

    def move_flying(self, strafe, forward, friction):
        f = np.float32(strafe * strafe + forward * forward)

        if f >= np.float32(1.0E-4):
            f = MathHelper.sqrt_float(f)

            if f < np.float32(1.0):
                f = np.float32(1.0)

            f = friction / f
            strafe = strafe * f
            forward = forward * f
            f1 = MathHelper.sin(self.rotation_yaw * np.float32(math.pi) / np.float32(180.0))
            f2 = MathHelper.cos(self.rotation_yaw * np.float32(math.pi) / np.float32(180.0))
            self.motion_x += np.float64(strafe * f2 - forward * f1)
            self.motion_z += np.float64(forward * f2 + strafe * f1)

    def on_update(self):
        self.on_entity_update()

    def on_entity_update(self):
        self.prev_distance_walked_modified = self.distance_walked_modified
        self.prev_pos_x = self.pos_x
        self.prev_pos_y = self.pos_y
        self.prev_pos_z = self.pos_z
        self.prev_rotation_pitch = self.rotation_pitch
        self.prev_rotation_yaw = self.rotation_yaw

        # self.handle_water_movement()

        # if self.is_in_lava():
        #     self.set_on_fire_from_lava()
        #     self.fall_distance *= np.float32(0.5)

        self.first_update = False
    
    def is_sneaking(self):
        return self.get_flag(1)
    
    def set_sneaking(self, sneaking):
        self.set_flag(1, sneaking)
    
    def is_sprinting(self):
        return self.get_flag(3)
    
    def set_sprinting(self, sprinting):
        self.set_flag(3, sprinting)
    
    def get_flag(self, flag):
        return self.data_watcher.get_watchable_object_byte(0) & 1 << flag != 0
    
    def set_flag(self, flag, set):
        b0 = self.data_watcher.get_watchable_object_byte(0)

        if set:
            self.data_watcher.update_object(0, np.int8(b0 | 1 << flag))
        else:
            self.data_watcher.update_object(0, np.int8(b0 & ~(1 << flag)))

    def get_entity_bounding_box(self):
        return self.bounding_box
    
    def set_entity_bounding_box(self, bb):
        self.bounding_box = bb

    def can_trigger_walking(self) -> bool:
        return True

    def update_fall_state(self, y: np.float64, on_ground_in: bool, block_in, pos):
        if on_ground_in:
            if self.fall_distance > np.float32(0.0):
                if block_in is not None:
                    block_in.on_fallen_upon(self.world_obj, pos, self, self.fall_distance)
                    pass
                else:
                    self.fall(self.fall_distance, np.float32(1.0))
                    pass
                self.fall_distance = np.float32(0.0)
        elif y < np.float64(0.0):
            self.fall_distance = np.float32(float(self.fall_distance) - float(y))

    def reset_position_to_BB(self):
        self.pos_x = (self.get_entity_bounding_box().min_x + self.get_entity_bounding_box().max_x) / np.float64(2.0)
        self.pos_y = self.get_entity_bounding_box().min_y
        self.pos_z = (self.get_entity_bounding_box().min_z + self.get_entity_bounding_box().max_z) / np.float64(2.0)

    def fall(self, distance, damage_multiplier):
        pass