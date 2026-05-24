from src.sim.util.vec3i import Vec3i


class EnumFacing:

    class Axis:
        def __init__(self, name: str):
            self.name = name

        def __str__(self) -> str:
            return self.name

    class AxisDirection:
        def __init__(self, offset: int, description: str):
            self._offset = offset
            self.description = description

        def get_offset(self) -> int:
            return self._offset

        def __str__(self) -> str:
            return self.description

    VALUES: list = [None] * 6
    HORIZONTALS: list = [None] * 4

    def __init__(self, index: int, opposite: int, horizontal_index: int, name: str,
                 axis_direction: 'EnumFacing.AxisDirection', axis: 'EnumFacing.Axis',
                 direction_vec: Vec3i):
        self.index = index
        self.opposite = opposite
        self.horizontal_index = horizontal_index
        self.name = name
        self.axis = axis
        self.axis_direction = axis_direction
        self.direction_vec = direction_vec

    def get_index(self) -> int:
        return self.index

    def get_horizontal_index(self) -> int:
        return self.horizontal_index

    def get_axis_direction(self) -> 'EnumFacing.AxisDirection':
        return self.axis_direction

    def get_opposite(self) -> 'EnumFacing':
        return EnumFacing.get_front(self.opposite)

    def get_front_offset_x(self) -> int:
        return self.axis_direction.get_offset() if self.axis is EnumFacing.Axis.X else 0

    def get_front_offset_y(self) -> int:
        return self.axis_direction.get_offset() if self.axis is EnumFacing.Axis.Y else 0

    def get_front_offset_z(self) -> int:
        return self.axis_direction.get_offset() if self.axis is EnumFacing.Axis.Z else 0

    def get_axis(self) -> 'EnumFacing.Axis':
        return self.axis

    def get_direction_vec(self) -> Vec3i:
        return self.direction_vec

    @staticmethod
    def get_front(index: int) -> 'EnumFacing':
        return EnumFacing.VALUES[abs(index % len(EnumFacing.VALUES))]

    def __str__(self) -> str:
        return self.name


EnumFacing.Axis.X = EnumFacing.Axis('x')
EnumFacing.Axis.Y = EnumFacing.Axis('y')
EnumFacing.Axis.Z = EnumFacing.Axis('z')

EnumFacing.AxisDirection.POSITIVE = EnumFacing.AxisDirection( 1, "Towards positive")
EnumFacing.AxisDirection.NEGATIVE = EnumFacing.AxisDirection(-1, "Towards negative")

EnumFacing.DOWN  = EnumFacing(0, 1, -1, "down",  EnumFacing.AxisDirection.NEGATIVE, EnumFacing.Axis.Y, Vec3i( 0, -1,  0))
EnumFacing.UP    = EnumFacing(1, 0, -1, "up",    EnumFacing.AxisDirection.POSITIVE, EnumFacing.Axis.Y, Vec3i( 0,  1,  0))
EnumFacing.NORTH = EnumFacing(2, 3,  2, "north", EnumFacing.AxisDirection.NEGATIVE, EnumFacing.Axis.Z, Vec3i( 0,  0, -1))
EnumFacing.SOUTH = EnumFacing(3, 2,  0, "south", EnumFacing.AxisDirection.POSITIVE, EnumFacing.Axis.Z, Vec3i( 0,  0,  1))
EnumFacing.WEST  = EnumFacing(4, 5,  1, "west",  EnumFacing.AxisDirection.NEGATIVE, EnumFacing.Axis.X, Vec3i(-1,  0,  0))
EnumFacing.EAST  = EnumFacing(5, 4,  3, "east",  EnumFacing.AxisDirection.POSITIVE, EnumFacing.Axis.X, Vec3i( 1,  0,  0))

for _f in [EnumFacing.DOWN, EnumFacing.UP, EnumFacing.NORTH, EnumFacing.SOUTH, EnumFacing.WEST, EnumFacing.EAST]:
    EnumFacing.VALUES[_f.index] = _f
    if _f.horizontal_index >= 0:
        EnumFacing.HORIZONTALS[_f.horizontal_index] = _f
