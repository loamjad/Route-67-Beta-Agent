class Material:
    def __init__(self):
        self.replaceable = False

    def set_replaceable(self):
        self.replaceable = True
        return self

Material.rock = Material()