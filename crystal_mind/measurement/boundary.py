from config.config_loader import config

class TopologicalBoundary:
    def __init__(self):
        self.U_min = config.get('boundary.U_min', 0.3)
        self.D_min = config.get('boundary.D_min', 0.4)
        self.A_max = config.get('boundary.A_max', 0.6)

    def check_margins(self, U, D, A):
        return {'U_margin':U-self.U_min, 'D_margin':D-self.D_min, 'A_margin':self.A_max-A}

    def is_within(self, U, D, A):
        return U>=self.U_min and D>=self.D_min and A<=self.A_max