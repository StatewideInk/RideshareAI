import networkx as nx
import matplotlib.pyplot as plt

seed = 1000;

G = nx.gnp_random_graph(200, 0.2, seed = seed);
print(G.nodes());