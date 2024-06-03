import networkx as nx
import random
from tqdm import tqdm
import matplotlib.pyplot as plt

def visualize_graph(triples,node_num=20):
    """
    Visualize a random sample of the triples in the dataset as a graph.
    
    Args:
        node_num (int): The number of nodes to include in the graph.
        
    Returns:
        None
    """
    # Create a new graph with a random sample of the triples
    G = nx.Graph()
    for h, r, t in tqdm(random.sample(triples, node_num)):
        G.add_edge(h, t, relation=r)
        
    # Use spring layout to position the nodes and draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=False)
    
    # Add edge labels to the graph
    labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    # Display the graph
    plt.show()