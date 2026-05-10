from src.sim.util.block_pos import BlockPos


class ChunkCoordIntPair:
    def __init__(self, x: int, z: int):
        self.chunk_x_pos: int = x
        self.chunk_z_pos: int = z

    @staticmethod
    def chunk_XZ2_int(x: int, z: int) -> int:
        return (x & 0xFFFFFFFF) | ((z & 0xFFFFFFFF) << 32)

    def __hash__(self) -> int:
        x = self.chunk_x_pos & 0xFFFFFFFF
        z = self.chunk_z_pos & 0xFFFFFFFF
        i = (1664525 * x + 1013904223) & 0xFFFFFFFF
        j = (1664525 * (z ^ 0xDEADBEEF) + 1013904223) & 0xFFFFFFFF
        return i ^ j

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, ChunkCoordIntPair):
            return False
        return self.chunk_x_pos == other.chunk_x_pos and self.chunk_z_pos == other.chunk_z_pos

    def get_center_x_pos(self) -> int:
        return (self.chunk_x_pos << 4) + 8

    def get_center_z_position(self) -> int:
        return (self.chunk_z_pos << 4) + 8

    def get_x_start(self) -> int:
        return self.chunk_x_pos << 4

    def get_z_start(self) -> int:
        return self.chunk_z_pos << 4

    def get_x_end(self) -> int:
        return (self.chunk_x_pos << 4) + 15

    def get_z_end(self) -> int:
        return (self.chunk_z_pos << 4) + 15

    def get_block(self, x: int, y: int, z: int) -> BlockPos:
        return BlockPos((self.chunk_x_pos << 4) + x, y, (self.chunk_z_pos << 4) + z)

    def get_center_block(self, y: int) -> BlockPos:
        return BlockPos(self.get_center_x_pos(), y, self.get_center_z_position())

    def __str__(self) -> str:
        return f"[{self.chunk_x_pos}, {self.chunk_z_pos}]"
