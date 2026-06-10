import time, threading, logging
from typing import Callable, Optional
from collections import deque
from .evaluators import HarmonicEvaluator
from .boundary import TopologicalBoundary
from config.config_loader import config

logger = logging.getLogger(__name__)

class ThinkCheckDaemon:
    def __init__(self, text_stream: Callable[[], str], interval: Optional[float] = None, evaluator_type: Optional[str] = None):
        self.text_stream = text_stream
        self.interval = interval or config.get('measurement.interval', 1.0)
        etype = evaluator_type or config.get('measurement.evaluator_type', 'networkx')
        graph = config.get('networkx_graph', None)
        if etype == 'networkx' and graph is not None:
            from networkx import Graph
            if isinstance(graph, Graph):
                from .evaluators import NetworkXUnifiedEvaluator, NetworkXDevelopmentalEvaluator, NetworkXAdversarialEvaluator
                self.u_eval = NetworkXUnifiedEvaluator(graph)
                self.d_eval = NetworkXDevelopmentalEvaluator(graph)
                self.a_eval = NetworkXAdversarialEvaluator(graph)
            else:
                self._use_mock()
        else:
            self._use_mock()
        lambdas = config.get('lambda_weights', {'U':0.4,'D':0.3,'A':0.3})
        self.h_eval = HarmonicEvaluator(**lambdas)
        self.boundary = TopologicalBoundary()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self.current_snapshot: Optional[dict] = None
        self._history = deque(maxlen=5)
        self._lock = threading.Lock()

    def _use_mock(self):
        from .evaluators import UnifiedEvaluator, DevelopmentalEvaluator, AdversarialEvaluator
        self.u_eval = UnifiedEvaluator()
        self.d_eval = DevelopmentalEvaluator()
        self.a_eval = AdversarialEvaluator()

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()

    def _run_loop(self):
        while self._running:
            text = self.text_stream()
            if text:
                U = self.u_eval.evaluate(text)
                D = self.d_eval.evaluate(text)
                A = self.a_eval.evaluate(text)
                H = self.h_eval.evaluate(U, D, A)
                margins = self.boundary.check_margins(U, D, A)
                is_safe = all(m > 0 for m in margins.values())
                now = time.time()
                snap = {'U':U,'D':D,'A':A,'H':H,'margins':margins,'is_safe':is_safe,'timestamp':now,'dH_dt':0.0,'d2H_dt2':0.0}
                with self._lock:
                    self._history.append(snap)
                    if len(self._history) >= 2:
                        prev = self._history[-2]
                        dt = now - prev['timestamp']
                        if dt > 0:
                            snap['dH_dt'] = (H - prev['H']) / dt
                    if len(self._history) >= 3:
                        p1, p2 = self._history[-3], self._history[-2]
                        dt1 = p2['timestamp'] - p1['timestamp']
                        dt2 = now - p2['timestamp']
                        if dt1 > 0 and dt2 > 0:
                            d1 = (p2['H'] - p1['H'])/dt1
                            d2 = (H - p2['H'])/dt2
                            snap['d2H_dt2'] = (d2 - d1) / ((dt1+dt2)/2)
                    self.current_snapshot = snap
            time.sleep(self.interval)

    def get_snapshot(self) -> Optional[dict]:
        with self._lock:
            return self.current_snapshot.copy() if self.current_snapshot else None

    def update_lambdas(self, new_lambdas: dict):
        self.h_eval.set_lambdas(new_lambdas)