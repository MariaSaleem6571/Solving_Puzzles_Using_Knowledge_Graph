import networkx as nx
import matplotlib.pyplot as plt

from rdflib import Graph, Namespace, URIRef, Literal, RDF, OWL


def create_rdf_graph():
    g = Graph()
    ns = Namespace("http://example.org/")

    # Define URIs for the individuals
    justin = URIRef(ns.Justin)
    oberon = URIRef(ns.Oberon)
    larry = URIRef(ns.Larry)
    xan = URIRef(ns.Xan)
    quentin = URIRef(ns.Quentin)
    hillary = URIRef(ns.Hillary)

    # Define classes
    knight = URIRef(ns.Knight)
    knave = URIRef(ns.Knave)

    # Define properties
    says = URIRef(ns.says)

    # Add classes
    g.add((knight, RDF.type, OWL.Class))
    g.add((knave, RDF.type, OWL.Class))

    # Add individuals
    for individual in [justin, oberon, larry, xan, quentin, hillary]:
        g.add((individual, RDF.type, OWL.NamedIndividual))

    # Add statements made by each individual
    g.add((larry, says, Literal("Justin is a knave")))
    g.add((oberon, says, Literal("Larry is a knave")))
    g.add((justin, says, Literal("Oberon always tells the truth")))
    g.add((xan, says, Literal("Quentin lies")))
    g.add((hillary, says, Literal("Xan is a knave")))
    g.add((quentin, says, Literal("Hillary is truthful")))
    g.add((larry, says, Literal("Quentin is a knight or I am a knave")))

    return g

# Create RDF graph
rdf_graph = create_rdf_graph()

# Create a NetworkX graph
G = nx.Graph()

# Add nodes (individuals)
for subj, _, _ in rdf_graph:
    G.add_node(subj)

# Add edges (relations)
for subj, pred, obj in rdf_graph:
    G.add_edge(subj, obj)

# Define positions for nodes using a layout algorithm (e.g., spring_layout)
pos = nx.spring_layout(G)

# Draw the graph with labels and customize the style
plt.figure(figsize=(10, 10))
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_size=10, font_color='black', font_weight='bold', edge_color='gray', width=1)

# Show the graph
plt.axis('off')
plt.title("Knowledge Graph Visualization")
plt.show()
