from models import d2l

class Pipline(d2l.HyperParameters):
    def __init__(self, data=d2l.DataModule, model=d2l.Module, trainer=d2l.Trainer):
        super().__init__()
        self.save_hyperparameters()
