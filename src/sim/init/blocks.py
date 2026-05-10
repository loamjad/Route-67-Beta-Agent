class Blocks:
    @classmethod
    def get_registered_block(cls, block):
        return Block.block

Blocks.air = Blocks.get_registered_block("air")
Blocks.stone = Blocks.get_registered_block("stone")