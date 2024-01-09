from rdflib import Graph, Namespace, URIRef, Literal, RDF, OWL

def create_rdf_graph():
    g = Graph()
    ns = Namespace("http://example.org/")

    # Entities
    houses = [URIRef(ns["House" + str(i)]) for i in range(1, 6)]
    colors = [ns.Red, ns.Green, ns.White, ns.Yellow, ns.Blue]
    nationalities = [ns.English, ns.Spanish, ns.Ukrainian, ns.Norwegian, ns.Japanese]
    animals = [ns.Dog, ns.Snail, ns.Fox, ns.Horse, ns.Zebra]
    drinks = [ns.Coffee, ns.Tea, ns.Milk, ns.OrangeJuice, ns.Water]
    smokes = [ns.OldGold, ns.Kool, ns.Chesterfield, ns.LuckyStrike, ns.Parliament]

    # Relationships
    same = URIRef(ns["same"])
    offset = URIRef(ns["offset"])
    dist = URIRef(ns["dist"])

    # Adding triples based on provided knowledge
    g.add((colors[0], same, nationalities[0]))  # Red - English
    g.add((nationalities[1], same, animals[0]))  # Spanish - Dog
    g.add((colors[1], same, drinks[0]))  # Green - Coffee
    g.add((nationalities[2], same, drinks[1]))  # Ukrainian - Tea
    g.add((houses[0], offset, colors[2]))  # House 1 - Offset - White - Green
    g.add((smokes[0], same, animals[1]))  # OldGold - Snail
    g.add((colors[3], same, smokes[1]))  # Yellow - Kool
    g.add((houses[2], same, drinks[2]))  # House 3 - Milk
    g.add((nationalities[3], same, houses[0]))  # Norwegian - House 1
    g.add((smokes[2], dist, animals[2]))  # Chesterfield - Dist - Fox
    g.add((animals[3], dist, smokes[1]))  # Horse - Dist - Kool
    g.add((smokes[3], same, drinks[3]))  # LuckyStrike - OrangeJuice
    g.add((nationalities[4], same, smokes[4]))  # Japanese - Parliament
    g.add((nationalities[3], dist, colors[4]))  # Norwegian - Dist - Blue

    return g

g = create_rdf_graph()

# Query to find which nationality drinks water
query_water = """
PREFIX ns: <http://example.org/>
SELECT ?nationality WHERE {
    ?nationality ns:same ns:Water .
}
"""

for row in g.query(query_water):
    print(f"Nationality that drinks water: {row.nationality}")

# Query to find which nationality keeps the zebra
query_zebra = """
PREFIX ns: <http://example.org/>
SELECT ?nationality WHERE {
    ?nationality ns:same ns:Zebra .
}
"""

for row in g.query(query_zebra):
    print(f"Nationality that keeps the zebra: {row.nationality}")
