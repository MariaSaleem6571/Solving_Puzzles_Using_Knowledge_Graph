from rdflib import Graph, Namespace, URIRef, Literal, RDF, OWL

def create_rdf_graph():
    g = Graph()
    ns = Namespace("http://example.org/")

    # Define URIs for the individuals
    hillary = URIRef(ns.Hillary)
    samuel = URIRef(ns.Samuel)
    vincent = URIRef(ns.Vincent)

    # Define classes
    knight = URIRef(ns.Knight)
    knave = URIRef(ns.Knave)

    # Define properties
    says = URIRef(ns.says)

    # Add classes
    g.add((knight, RDF.type, OWL.Class))
    g.add((knave, RDF.type, OWL.Class))

    # Add individuals
    for individual in [hillary, samuel, vincent]:
        g.add((individual, RDF.type, OWL.NamedIndividual))

    # Add statements made by each individual
    g.add((samuel, says, Literal("Hillary is a Knave")))
    g.add((hillary, says, Literal("Vincent is a Knave")))
    g.add((vincent, says, Literal("Samuel is a Knight and I am a Knave")))

    return g

