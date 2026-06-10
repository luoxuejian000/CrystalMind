class Sandbox:
    def __init__(self): self.results = []
    def run_test(self, func, input_data) -> bool:
        try:
            out = func(input_data)
            self.results.append({'passed':True,'output':out})
            return True
        except Exception as e:
            self.results.append({'passed':False,'error':str(e)})
            return False