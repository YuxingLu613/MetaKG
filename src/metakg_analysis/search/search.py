import json

def search(triples,node_list, selected_relations, show_only=3,save_results=False,save_path="outputs/lookup.json"):
    """Lookup triplets based on specified nodes and relations and display the results.

    Args:
        node_list (list): List of nodes to include in search.
        selected_relations (list): List of relations to include in search.
        show_only (int, optional): Number of tail nodes to display. Defaults to 3.

    Returns:
        None
    """
    relation_count = {}

    for h, r, t in triples:
        if h in node_list and r in selected_relations:
            if r not in relation_count:
                relation_count[r] = {}
            if t not in relation_count[r]:
                relation_count[r][t] = 0
            relation_count[r][t] += 1

    lookup_result={}
    
    for r, tail_nodes in relation_count.items():
        if save_results:
            lookup_result[r]=tail_nodes
        sorted_tail_nodes = sorted(tail_nodes.items(), key=lambda x: x[1], reverse=True)
        print(f"Relation: {r}")
        for t, count in sorted_tail_nodes[:show_only]:
            print(f"  Tail Node: {t} Count: {count}")
    
    if save_results:
        print(f"lookup results saved to {save_path}")
        with open(save_path, "w") as f:
            json.dump(lookup_result, f)
    return sorted_tail_nodes[:show_only]
            
            
def search_backward(triples,node_list, selected_relations, show_only=3,save_results=False,save_path="outputs/lookup_backward.json"):
    """Lookup triplets based on specified nodes and relations in backward direction and display the results.

    Args:
        node_list (list): List of nodes to include in search.
        selected_relations (list): List of relations to include in search.
        show_only (int, optional): Number of tail nodes to display. Defaults to 3.

    Returns:
        None
    """
    relation_count = {}

    for h, r, t in triples.values.tolist():
        if t in node_list and r in selected_relations:
            if r not in relation_count:
                relation_count[r] = {}
            if h not in relation_count[r]:
                relation_count[r][h] = 0
            relation_count[r][h] += 1

    lookup_result={}
    
    for r, head_nodes in relation_count.items():
        if save_results:
            lookup_result[r]=head_nodes
        sorted_head_nodes = sorted(head_nodes.items(), key=lambda x: x[1], reverse=True)
        print(f"Relation: {r}")
        for h, count in sorted_head_nodes[:show_only]:
            print(f"  Head Node: {h} Count: {count}")
    
    if save_results:
        print(f"lookup results saved to {save_path}")
        with open(save_path, "w") as f:
            json.dump(lookup_result, f)    
    return sorted_head_nodes[:show_only]