from src.sim.entity.player.entity_player import EntityPlayer

class AbstractClientPlayer(EntityPlayer):
    def __init__(self, world_in):
        super().__init__(world_in)