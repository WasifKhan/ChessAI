from ai.models.base_model import BaseModel


class LabeebAI(BaseModel):
    def __init__(self, game, location):
        super().__init__(game, location)

    def train(self):
        return True

    def predict(self, board, is_white):
        return NotImplemented


