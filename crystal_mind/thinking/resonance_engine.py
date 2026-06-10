import logging
from config.config_loader import config

logger = logging.getLogger(__name__)

class ResonanceEngine:
    def __init__(self, alpha=None, beta=None, gamma=None):
        self.alpha = alpha or config.get('resonance_engine.alpha', 0.1)
        self.beta  = beta  or config.get('resonance_engine.beta', 0.05)
        self.gamma = gamma or config.get('resonance_engine.gamma', 0.02)
        self.tau   = config.get('resonance_engine.initial_temperature', 1.0)

    def update_temperature(self, dH_dt: float, d2H_dt2: float) -> float:
        delta = -self.alpha*(dH_dt/self.tau if self.tau else 0) + self.beta*d2H_dt2 - self.gamma*self.tau
        self.tau += delta*0.1
        self.tau = max(0.1, min(2.0, self.tau))
        return self.tau

    def generate_strategy(self, snapshot: dict) -> dict:
        H = snapshot['H']
        dH = snapshot.get('dH_dt',0.0)
        d2H = snapshot.get('d2H_dt2',0.0)
        new_tau = self.update_temperature(dH, d2H)
        adj = {}
        if H < 0.5:
            adj['U'] = +0.05
            adj['A'] = -0.05
        elif H < 0.8:
            if snapshot.get('A',0) > 0.3:
                adj['A'] = -0.03
                adj['D'] = +0.03
        else:
            adj['D'] = -0.02
        return {'adjust_lambda': adj, 'new_temperature': new_tau}