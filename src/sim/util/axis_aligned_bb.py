import numpy as np


class AxisAlignedBB:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.min_x = min(x1, x2)
        self.min_y = min(y1, y2)
        self.min_z = min(z1, z2)
        self.max_x = max(x1, x2)
        self.max_y = max(y1, y2)
        self.max_z = max(z1, z2)

    def intersects_with(self, other: 'AxisAlignedBB') -> bool:
        return (other.max_x > self.min_x and other.min_x < self.max_x and
                other.max_y > self.min_y and other.min_y < self.max_y and
                other.max_z > self.min_z and other.min_z < self.max_z)

    def add_coord(self, x: np.float64, y: np.float64, z: np.float64) -> 'AxisAlignedBB':
        d0, d1, d2 = self.min_x, self.min_y, self.min_z
        d3, d4, d5 = self.max_x, self.max_y, self.max_z

        if x < np.float64(0.0):
            d0 += x
        elif x > np.float64(0.0):
            d3 += x

        if y < np.float64(0.0):
            d1 += y
        elif y > np.float64(0.0):
            d4 += y

        if z < np.float64(0.0):
            d2 += z
        elif z > np.float64(0.0):
            d5 += z

        return AxisAlignedBB(d0, d1, d2, d3, d4, d5)

    def calculate_x_offset(self, other: 'AxisAlignedBB', offset_x: float) -> float:
        if other.max_y > self.min_y and other.min_y < self.max_y and other.max_z > self.min_z and other.min_z < self.max_z:
            if offset_x > np.float64(0.0) and other.max_x <= self.min_x:
                d1 = self.min_x - other.max_x
                if d1 < offset_x:
                    offset_x = d1
            elif offset_x < np.float64(0.0)and other.min_x >= self.max_x:
                d0 = self.max_x - other.min_x
                if d0 > offset_x:
                    offset_x = d0
        return offset_x

    def calculate_y_offset(self, other: 'AxisAlignedBB', offset_y: float) -> float:
        if other.max_x > self.min_x and other.min_x < self.max_x and other.max_z > self.min_z and other.min_z < self.max_z:
            if offset_y > np.float64(0.0)and other.max_y <= self.min_y:
                d1 = self.min_y - other.max_y
                if d1 < offset_y:
                    offset_y = d1
            elif offset_y < np.float64(0.0)and other.min_y >= self.max_y:
                d0 = self.max_y - other.min_y
                if d0 > offset_y:
                    offset_y = d0
        return offset_y

    def calculate_z_offset(self, other: 'AxisAlignedBB', offset_z: float) -> float:
        if other.max_x > self.min_x and other.min_x < self.max_x and other.max_y > self.min_y and other.min_y < self.max_y:
            if offset_z > np.float64(0.0)and other.max_z <= self.min_z:
                d1 = self.min_z - other.max_z
                if d1 < offset_z:
                    offset_z = d1
            elif offset_z < np.float64(0.0)and other.min_z >= self.max_z:
                d0 = self.max_z - other.min_z
                if d0 > offset_z:
                    offset_z = d0
        return offset_z

    def offset(self, x, y, z):
        return AxisAlignedBB(
            self.min_x + x,
            self.min_y + y,
            self.min_z + z,
            self.max_x + x,
            self.max_y + y,
            self.max_z + z,
        )
