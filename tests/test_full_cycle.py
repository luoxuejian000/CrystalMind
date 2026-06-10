import time, networkx as nx
from crystal_mind.measurement.thinkcheck_daemon import ThinkCheckDaemon
from crystal_mind.thinking.resonance_engine import ResonanceEngine
from crystal_mind.execution.photon_scheduler import PhotonScheduler
from crystal_mind.execution.tool_catalog import ToolCatalog, ToolRecord
from config.config_loader import config

def test_full_cycle():
    G = nx.Graph()
    G.add_nodes_from(['x','y','z'])
    G.add_edge('x','y', weight=0.8)
    G.add_edge('y','z', weight=-0.4)
    config._config['networkx_graph'] = G
    daemon = ThinkCheckDaemon(lambda: "sim", interval=0.2, evaluator_type='networkx')
    daemon.start()
    engine = ResonanceEngine()
    catalog = ToolCatalog()
    scheduler = PhotonScheduler(catalog)
    catalog.add(ToolRecord("t1","1",lambda x:x,"str","str",[],{}))
    catalog.approve("t1")
    time.sleep(0.8)
    snap = daemon.get_snapshot()
    assert snap is not None
    strategy = engine.generate_strategy(snap)
    if strategy['adjust_lambda']:
        cur = daemon.h_eval.lambdas
        new = {k: max(0.1, cur[k]+v) for k,v in strategy['adjust_lambda'].items()}
        total = sum(new.values())
        new = {k:v/total for k,v in new.items()}
        daemon.update_lambdas(new)
    res = scheduler.execute_tool("t1", "data")
    assert res == "data"
    daemon.stop()