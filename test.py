import networkx as nx

g = nx.Graph()


g.add_node(1)
g.add_nodes_from([2,3])
g.add_nodes_from([2,3])

g.add_edge(1, 2, weight=3)
e = (2, 3)
g.add_edge(*e)

print g[1][2]['weight']
print g.edges
