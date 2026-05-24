from src.sim.util.vec3i import Vec3i
from src.sim.util.enum_facing import EnumFacing

class BlockPos(Vec3i):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)

    def offset(self, facing: EnumFacing, n: int = 1) -> 'BlockPos':
        if n == 0:
            return self
        return BlockPos(
            self.x + facing.get_front_offset_x() * n,
            self.y + facing.get_front_offset_y() * n,
            self.z + facing.get_front_offset_z() * n
        )

    def down(self, n: int = 1) -> 'BlockPos':
        return self.offset(EnumFacing.DOWN, n)

    class MutableBlockPos(Vec3i):
        def __init__(self, x: int = 0, y: int = 0, z: int = 0):
            super().__init__(0, 0, 0)
            self.x = x
            self.y = y
            self.z = z

        def get_x(self) -> int:
            return self.x

        def get_y(self) -> int:
            return self.y

        def get_z(self) -> int:
            return self.z

        def set(self, x: int, y: int, z: int) -> 'BlockPos.MutableBlockPos':
            self.x = x
            self.y = y
            self.z = z
            return self