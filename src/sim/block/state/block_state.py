from src.sim.block.state.block_state_base import BlockStateBase

class BlockState(BlockStateBase):
    def __init__(self, block_in):
        self.valid_states = []

        self.block = block_in

        self.valid_states.append(self.create_state(block_in))

    def get_block(self):
        return self.block
    
    def get_base_state(self):
        return self.valid_states[0]
    
    def create_state(self, block):
        return StateImplementation(block)

class StateImplementation(BlockStateBase):
    def __init__(self, block_in):
        self.block = block_in

    def get_block(self):
        return self.block