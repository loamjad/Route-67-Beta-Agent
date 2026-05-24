import pytest
import numpy as np
from src.agent import Agent
from src.sim.client.minecraft import Minecraft

class TestAgent:
    def test_run(self):
        mc = Minecraft()
        player = mc.the_player
        world = mc.the_world
        world.mc = self

        input_dict = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "sneak": False,
            "jump": False,
            "sprint": False
        }

        player.run_tick()
        print(player.get_pos())
