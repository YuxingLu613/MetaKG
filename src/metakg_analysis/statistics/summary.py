import networkx as nx
from tqdm import tqdm
from collections import Counter
import json
from .utils import draw_statistics


import networkx as nx
from collections import Counter
import json
import matplotlib.pyplot as plt
from tqdm import tqdm

def summary(triples, show_bar_graph=True, save_result=False, topk=20):
    """Summarizes the statistics of the knowledge graph and saves them to a JSON file.

    Args:
        show_bar_graph (bool): Whether to display the bar graph of the frequency count. Default is True.
        topk (int): The number of top-k items to show in the bar graph. Default is 20.

    Returns:
        None.

    """
    statistics = {}

    G = nx.Graph()
    for h, r, t in tqdm(triples.values.tolist()):
        G.add_edge(h, t, relation=r)

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    print("Number of nodes:", num_nodes)
    print("Number of edges:", num_edges)
    statistics["Nodes number"] = num_nodes
    statistics["Edges number"] = num_edges

    relation_counter = Counter([data['relation'] for u, v, data in G.edges(data=True)])
    head_counter = Counter([u for u, v, data in G.edges(data=True)])
    tail_counter = Counter([v for u, v, data in G.edges(data=True)])

    statistics[f"Top {topk} Relations"] = sorted(relation_counter.items(), key=lambda x: x[1], reverse=True)[:topk]
    statistics[f"Top {topk} Head Entities"] = sorted(head_counter.items(), key=lambda x: x[1], reverse=True)[:topk]
    statistics[f"Top {topk} Tail Entities"] = sorted(tail_counter.items(), key=lambda x: x[1], reverse=True)[:topk]

    # 稀疏度计算
    sparsity = nx.density(G)
    print("Sparsity:", sparsity)
    statistics["Sparsity"] = sparsity

    # 连通性分析
    connected_components = list(nx.connected_components(G))
    num_connected_components = len(connected_components)
    largest_component = max(connected_components, key=len)
    largest_component_size = len(largest_component)

    print("Number of connected components:", num_connected_components)
    print("Size of the largest component:", largest_component_size)

    statistics["Number of connected components"] = num_connected_components
    statistics["Size of the largest component"] = largest_component_size

    if show_bar_graph:
        draw_statistics(relation_counter, "relations", topk)
        draw_statistics(head_counter, "heads", topk)
        draw_statistics(tail_counter, "tails", topk)

    if save_result:
        print("statistics results saved to outputs/statistics.json")
        with open("outputs/statistics.json", "w") as f:
            json.dump(statistics, f)
