#!/usr/bin/env python3
"""故事化演示：生态攻防演练"""
import time, networkx as nx, logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from crystal_mind.measurement.evaluators import (
    NetworkXUnifiedEvaluator, NetworkXDevelopmentalEvaluator,
    NetworkXAdversarialEvaluator, HarmonicEvaluator
)
from crystal_mind.thinking.resonance_engine import ResonanceEngine

console = Console()
logging.basicConfig(level=logging.WARNING)

def print_status(phase, u, d, a, h, lambdas, tau):
    table = Table(title=f"📊 {phase}")
    table.add_column("指标", style="cyan")
    table.add_column("数值", style="magenta")
    table.add_column("趋势", style="green")
    table.add_row("U 统一性", f"{u:.3f}", "凝聚力" + ("↑" if u > 0.5 else "↓"))
    table.add_row("D 发展性", f"{d:.3f}", "多样性" + ("↑" if d > 0.3 else "↓"))
    table.add_row("A 对抗性", f"{a:.3f}", "冲突度" + ("⚠️" if a > 0.3 else "✓"))
    table.add_row("H 和谐度", f"{h:.3f}", "综合" + ("✓" if h > 0.5 else "⚠️"))
    table.add_row("λ 权重", f"U:{lambdas['U']:.2f} D:{lambdas['D']:.2f} A:{lambdas['A']:.2f}", "")
    table.add_row("τ 温度", f"{tau:.2f}", "探索强度")
    console.print(table)

def main():
    console.print(Panel.fit("🧠 CrystalMind 故事化演示：生态攻防演练", style="bold cyan"))
    G = nx.Graph()
    G.add_nodes_from(['agent-1','agent-2','agent-3','site-a','site-b'])
    G.add_edge('agent-1','site-a', weight=0.9)
    G.add_edge('agent-2','site-a', weight=0.7)
    G.add_edge('agent-3','site-b', weight=0.6)
    u_eval = NetworkXUnifiedEvaluator(G)
    d_eval = NetworkXDevelopmentalEvaluator(G)
    a_eval = NetworkXAdversarialEvaluator(G)
    h_eval = HarmonicEvaluator()
    engine = ResonanceEngine()

    u = u_eval.evaluate()
    d = d_eval.evaluate()
    a = a_eval.evaluate()
    h = h_eval.evaluate(u,d,a)
    console.print("\n[bold green]🌱 第一幕：健康生态[/bold green]")
    console.print("一个拥有 5 个节点的数据生态，3 个 Agent 与 2 个站点和谐协作。")
    print_status("初始状态", u, d, a, h, h_eval.lambdas, engine.tau)
    time.sleep(1.5)

    console.print("\n[bold red]💣 第二幕：恶意攻击[/bold red]")
    console.print("黑客 agent-3 突然向 agent-1 和 agent-2 发起恶意数据窃取！")
    G.add_edge('agent-3','agent-1', weight=-0.95)
    G.add_edge('agent-3','agent-2', weight=-0.85)
    u_eval = NetworkXUnifiedEvaluator(G)
    d_eval = NetworkXDevelopmentalEvaluator(G)
    a_eval = NetworkXAdversarialEvaluator(G)
    u = u_eval.evaluate()
    d = d_eval.evaluate()
    a = a_eval.evaluate()
    h = h_eval.evaluate(u,d,a)
    print_status("遭受攻击后", u, d, a, h, h_eval.lambdas, engine.tau)
    time.sleep(1.5)

    console.print("\n[bold yellow]⚙️ 第三幕：系统自愈[/bold yellow]")
    console.print("CrystalMind 谐振引擎检测到 A 值飙升，自动启动调谐...")
    for cycle in range(4):
        snap = {'U':u,'D':d,'A':a,'H':h,'dH_dt':0,'d2H_dt2':0}
        strategy = engine.generate_strategy(snap)
        if strategy['adjust_lambda']:
            cur = h_eval.lambdas
            new = {}
            for k in ['U','D','A']:
                new[k] = max(0.1, cur.get(k,0.4) + strategy['adjust_lambda'].get(k,0))
            s = sum(new.values())
            new = {k:v/s for k,v in new.items()}
            h_eval.set_lambdas(new)
        time.sleep(0.5)
        u = u_eval.evaluate()
        d = d_eval.evaluate()
        a = a_eval.evaluate()
        h = h_eval.evaluate(u,d,a)
        console.print(f"  调谐周期 {cycle+1}: H={h:.3f} | λ=({h_eval.lambdas['U']:.2f},{h_eval.lambdas['D']:.2f},{h_eval.lambdas['A']:.2f}) | τ={engine.tau:.2f}")

    console.print("\n[bold green]✅ 第四幕：康复平衡[/bold green]")
    console.print("系统通过自适应调谐，在对抗与协作之间找到了新的平衡点。")
    print_status("自愈完成后", u, d, a, h, h_eval.lambdas, engine.tau)

    console.print("\n[bold cyan]🎉 演示结束[/bold cyan]")
    console.print("CrystalMind 核心价值：让系统拥有自我感知、自我修复的智能内核。")

if __name__ == '__main__':
    main()