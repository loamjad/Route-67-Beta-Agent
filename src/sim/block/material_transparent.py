from src.sim.block.material import Material

class MaterialTransparent(Material):
    def __init__(self):
        super().__init__()
        self.set_replaceable()