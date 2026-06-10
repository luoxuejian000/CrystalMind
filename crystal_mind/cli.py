import click, json, networkx as nx, logging
from crystal_mind.measurement.evaluators import (
    NetworkXUnifiedEvaluator, NetworkXDevelopmentalEvaluator,
    NetworkXAdversarialEvaluator, HarmonicEvaluator
)
from rich.console import Console
from rich.table import Table

console = Console()
logging.basicConfig(level=logging.INFO)

@click.group()
def main():
    """CrystalMind —— 智能安全内核 CLI"""
    pass

@main.command()
def demo():
    """运行故事化演示"""
    from crystal_mind.demo_story import main as dm
    dm()

@main.command()
def dashboard():
    """启动可视化仪表盘"""
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "streamlit", "run", "crystal_mind/dashboard.py"])

@main.command()
def test():
    """运行测试"""
    import pytest, sys
    sys.exit(pytest.main(['tests','-v']))

@main.command()
@click.option('--graph', required=True, help='Path to graph JSON file')
def evaluate(graph):
    """评估网络图的健康度"""
    with open(graph) as f:
        data = json.load(f)
    G = nx.Graph()
    for n in data.get('nodes',[]):
        G.add_node(n['id'])
    for e in data.get('edges',[]):
        G.add_edge(e['source'], e['target'], weight=e.get('weight',1))
    u = NetworkXUnifiedEvaluator(G).evaluate()
    d = NetworkXDevelopmentalEvaluator(G).evaluate()
    a = NetworkXAdversarialEvaluator(G).evaluate()
    h = HarmonicEvaluator().evaluate(u,d,a)
    table = Table(title="生态健康度评估")
    table.add_column("指标", style="cyan")
    table.add_column("数值", style="magenta")
    table.add_column("解读", style="green")
    table.add_row("U (统一性)", f"{u:.3f}", "正面连接的凝聚力")
    table.add_row("D (发展性)", f"{d:.3f}", "跨社区的桥接多样性")
    table.add_row("A (对抗性)", f"{a:.3f}", "负面关系的冲突程度")
    table.add_row("H (和谐度)", f"{h:.3f}", "综合谐振指数")
    console.print(table)

if __name__ == '__main__':
    main()