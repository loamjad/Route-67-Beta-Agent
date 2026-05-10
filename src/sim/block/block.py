import numpy as np

class Block:
    def __init__(self):
        self.slipperiness = np.float32(0.6)
        self.default_block_state = None
        
        self.set_default_state(self.block_state.get_base_state())

    def get_default_state(self):
        return self.default_block_state
    
    def set_default_state(self, state):
        self.default_block_state = state