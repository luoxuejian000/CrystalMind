import time
from crystal_mind.measurement.thinkcheck_daemon import ThinkCheckDaemon

def test_daemon_mock():
    daemon = ThinkCheckDaemon(lambda: "test", interval=0.1, evaluator_type='mock')
    daemon.start()
    time.sleep(0.4)
    snap = daemon.get_snapshot()
    assert snap and 'U' in snap and 'dH_dt' in snap
    daemon.stop()