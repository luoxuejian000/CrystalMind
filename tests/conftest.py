import pytest, networkx as nx

@pytest.fixture
def sample_graph():
    G = nx.Graph()
    G.add_nodes_from(['a','b','c'])
    G.add_edge('a','b', weight=0.9)
    G.add_edge('b','c', weight=-0.5)
    return G