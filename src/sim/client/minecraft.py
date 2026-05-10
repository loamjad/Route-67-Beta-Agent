from src.sim.client.multiplayer.world_client import WorldClient
from src.sim.client.entity.entity_player_sp import EntityPlayerSP

class Minecraft:
    def __init__(self):
        self.the_world = None
        self.the_player = None

        self.the_world = WorldClient()
        self.the_player = EntityPlayerSP()