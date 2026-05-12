import pytest
import numpy as np
from src.agent import Agent


@pytest.fixture
def agent():
    return Agent()


class TestInit:
    def test_initial_position_is_zero(self, agent):
        assert agent.get_pos() == (np.float64(0.0), np.float64(0.0), np.float64(0.0))

    def test_initial_motion_is_zero(self, agent):
        assert agent.get_motion() == (np.float64(0.0), np.float64(0.0), np.float64(0.0))

    def test_initial_rotation_is_zero(self, agent):
        assert agent.get_rotation() == (np.float32(0.0), np.float32(0.0))


class TestSetPosition:
    def test_set_position(self, agent):
        agent.set_position(1.0, 64.0, -5.0)
        x, y, z = agent.get_pos()
        assert x == pytest.approx(1.0)
        assert y == pytest.approx(64.0)
        assert z == pytest.approx(-5.0)


class TestSetRotation:
    def test_set_rotation(self, agent):
        agent.set_rotation(90.0, 45.0)
        yaw, pitch = agent.get_rotation()
        assert float(yaw) == pytest.approx(90.0)
        assert float(pitch) == pytest.approx(45.0)


class TestSetInputs:
    def test_non_bool_input_raises(self, agent):
        with pytest.raises(TypeError):
            agent.set_inputs({"w": 1})

    def test_all_false_inputs_accepted(self, agent):
        agent.set_inputs({"w": False, "a": False, "s": False, "d": False,
                          "jump": False, "sneak": False, "sprint": False})

    def test_partial_inputs_use_defaults(self, agent):
        agent.set_inputs({"w": True})
        settings = agent.player.movement_input.game_settings
        assert settings.key_bind_forward.pressed is True
        assert settings.key_bind_left.pressed is False

    def test_all_inputs_set(self, agent):
        agent.set_inputs({"w": True, "a": True, "s": True, "d": True,
                          "jump": True, "sneak": True, "sprint": True})
        s = agent.player.movement_input.game_settings
        assert s.key_bind_forward.pressed is True
        assert s.key_bind_left.pressed is True
        assert s.key_bind_back.pressed is True
        assert s.key_bind_right.pressed is True
        assert s.key_bind_jump.pressed is True
        assert s.key_bind_sneak.pressed is True
        assert s.key_bind_sprint.pressed is True


class TestRunTick:
    def test_tick_advances_last_tick_pos(self, agent):
        agent.set_position(5.0, 64.0, 3.0)
        agent.run_tick()
        last = agent.get_last_tick_pos()
        assert last[0] == pytest.approx(5.0)
        assert last[1] == pytest.approx(64.0)
        assert last[2] == pytest.approx(3.0)

    def test_tick_applies_gravity_when_airborne(self, agent):
        agent.player.on_ground = False
        agent.run_tick()
        _, motion_y, _ = agent.get_motion()
        assert motion_y < 0.0

    def test_forward_input_produces_positive_z_motion(self, agent):
        agent.set_rotation(0.0, 0.0)
        agent.set_inputs({"w": True})
        agent.run_tick()
        _, _, motion_z = agent.get_motion()
        assert motion_z > 0.0
