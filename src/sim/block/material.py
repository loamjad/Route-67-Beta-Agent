from src.sim.block.material_transparent import MaterialTransparent

class Material:
    def __init__(self):
        self.replaceable = False

    def set_replaceable(self):
        self.replaceable = True
        return self

Material.air = MaterialTransparent()
Material.rock = Material()