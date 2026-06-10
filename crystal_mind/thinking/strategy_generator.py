class StrategyGenerator:
    def generate(self, snapshot: dict) -> dict:
        margins = snapshot.get('margins',{})
        actions = []
        if margins.get('A_margin',1) < 0.05:
            actions.append({'action':'release_tool','reason':'A margin low'})
        return {'actions':actions}