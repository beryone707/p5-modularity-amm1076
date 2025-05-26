"""
File name: assignment.py
Description: function to compute the modularity of a graph and to detect communities by Girvan-Newman algorithm

Authors:
    - Berivan Alpagu (bax1020@alu.ubu.es)
    
License:
    This script is licensed under the MIT License. 
    https://opensource.org/licenses/MIT
"""

import networkx as nx
import numpy as np
import pandas as pd


# Function to compute the modularity of a graph
def modularity(G,partition):
# Your code here
m = G.number_of_edges()
    if m == 0:
        return 0.0
    
    degrees = dict(G.degree())
    total_degree = sum(degrees.values())
    Q = 0.0
    
    for community in partition:
        sum_in = 0
        sum_tot = 0
        for node in community:
            sum_tot += degrees[node]
            for neighbor in G.neighbors(node):
                if neighbor in community:
                    sum_in += 1
        
        Q += (sum_in / (2*m)) - (sum_tot / (2*m))**2
    return Q



# Function to detect communities by Girvan-Newman algorithm
def girvan_newman_communities(G):
# Your code here
original = G.copy()
    current = original.copy()
    best_partition = [set(original.nodes())]
    best_q = modularity(original, best_partition)
    q_history = [best_q]
    
    steps_data = []
    
    while current.number_of_edges() > 0:
        eb = nx.edge_betweenness_centrality(current)
        max_eb = max(eb.values())
        edge_to_remove = [e for e, val in eb.items() if val == max_eb][0]
        current.remove_edge(*edge_to_remove)
        
        components = list(nx.connected_components(current))
        if len(components) > len(best_partition):
            q = modularity(original, components)
            q_history.append(q)
            steps_data.append({
                'edge_removed': edge_to_remove,
                'communities': components,
                'modularity': q
            })
            if q > best_q:
                best_q = q
                best_partition = components
    
    steps_df = pd.DataFrame(steps_data)

    return best_partition, best_q, q_history, steps_df
