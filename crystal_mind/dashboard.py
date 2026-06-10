"""CrystalMind 可视化仪表盘"""
import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time, collections
from crystal_mind.measurement.evaluators import (
    NetworkXUnifiedEvaluator, NetworkXDevelopmentalEvaluator,
    NetworkXAdversarialEvaluator, HarmonicEvaluator
)
from crystal_mind.thinking.resonance_engine import ResonanceEngine

st.set_page_config(page_title="CrystalMind 仪表盘", layout="wide")
st.title("🧠 CrystalMind 生态健康度仪表盘")

if 'engine' not in st.session_state:
    st.session_state.engine = ResonanceEngine()
if 'history' not in st.session_state:
    st.session_state.history = collections.deque(maxlen=100)
if 'running' not in st.session_state:
    st.session_state.running = False
if 'graph' not in st.session_state:
    G = nx.Graph()
    G.add_nodes_from(['agent-1','agent-2','agent-3','site-a','site-b'])
    G.add_edge('agent-1','site-a', weight=0.9)
    G.add_edge('agent-2','site-a', weight=0.7)
    G.add_edge('agent-3','site-b', weight=-0.4)
    st.session_state.graph = G
    st.session_state.u_eval = NetworkXUnifiedEvaluator(G)
    st.session_state.d_eval = NetworkXDevelopmentalEvaluator(G)
    st.session_state.a_eval = NetworkXAdversarialEvaluator(G)
    st.session_state.h_eval = HarmonicEvaluator()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button('▶️ 启动监控'):
        st.session_state.running = True
with col2:
    if st.button('⏹️ 停止监控'):
        st.session_state.running = False
with col3:
    if st.button('💣 模拟攻击'):
        G = st.session_state.graph
        G.add_edge('agent-3','agent-1', weight=-0.9)
        G.add_edge('agent-3','agent-2', weight=-0.8)
        st.session_state.u_eval = NetworkXUnifiedEvaluator(G)
        st.session_state.d_eval = NetworkXDevelopmentalEvaluator(G)
        st.session_state.a_eval = NetworkXAdversarialEvaluator(G)
        st.success('攻击已注入！观察系统如何自愈...')

chart_placeholder = st.empty()
metrics_placeholder = st.empty()
log_placeholder = st.empty()

while st.session_state.running:
    u = st.session_state.u_eval.evaluate()
    d = st.session_state.d_eval.evaluate()
    a = st.session_state.a_eval.evaluate()
    h = st.session_state.h_eval.evaluate(u,d,a)
    snap = {'U':u,'D':d,'A':a,'H':h,'timestamp':time.time()}
    st.session_state.history.append(snap)
    strategy = st.session_state.engine.generate_strategy({'H':h,'A':a,'dH_dt':0,'d2H_dt2':0})
    if strategy['adjust_lambda']:
        cur = st.session_state.h_eval.lambdas
        new = {}
        for k in ['U','D','A']:
            new[k] = max(0.1, cur.get(k,0.4) + strategy['adjust_lambda'].get(k,0))
        s = sum(new.values())
        new = {k:v/s for k,v in new.items()}
        st.session_state.h_eval.set_lambdas(new)
    with metrics_placeholder.container():
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("U 统一性", f"{u:.3f}")
        m2.metric("D 发展性", f"{d:.3f}")
        m3.metric("A 对抗性", f"{a:.3f}", delta=f"{a-0.1:.3f}" if a>0.3 else None)
        m4.metric("H 和谐度", f"{h:.3f}")
    with chart_placeholder.container():
        if len(st.session_state.history) > 1:
            hist = list(st.session_state.history)
            fig = make_subplots(rows=2, cols=2)
            fig.add_trace(go.Scatter(y=[x['U'] for x in hist], name='U', line=dict(color='blue')), row=1, col=1)
            fig.add_trace(go.Scatter(y=[x['D'] for x in hist], name='D', line=dict(color='green')), row=1, col=2)
            fig.add_trace(go.Scatter(y=[x['A'] for x in hist], name='A', line=dict(color='red')), row=2, col=1)
            fig.add_trace(go.Scatter(y=[x['H'] for x in hist], name='H', line=dict(color='purple')), row=2, col=2)
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    with log_placeholder.container():
        st.caption(f"最新快照: U={u:.3f} D={d:.3f} A={a:.3f} H={h:.3f} | 温度 τ={st.session_state.engine.tau:.2f}")
    time.sleep(1)
    st.rerun()